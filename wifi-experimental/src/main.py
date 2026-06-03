import socket
import select
import gc
import time
import json
import math
import random
import machine
import rmt_neopixel
from config import LOOKUP
import presets

PIN = 13
COUNT = 64
IDLE_MS = 30000
ACTIVE_FILE = "active.json"

np = rmt_neopixel.NeoPixel(machine.Pin(PIN, machine.Pin.OUT), COUNT)

state = {
    "fn": None,
    "name": "off",
    "frame": 0,
    "last_tick": 0,
    "error": "",
    "tick_ms": 120,
    "last_activity": time.ticks_ms(),
    "dark": False,
    "custom_code": "",
}


def mark_activity():
    state["last_activity"] = time.ticks_ms()


def save_active():
    payload = {"name": state["name"]}
    if state["name"] == "custom":
        payload["code"] = state["custom_code"]
    try:
        with open(ACTIVE_FILE, "w") as f:
            json.dump(payload, f)
    except Exception as e:
        print("save_active err:", e)


def load_active():
    try:
        with open(ACTIVE_FILE, "r") as f:
            return json.load(f)
    except:
        return None


def clear():
    for i in range(COUNT):
        np[i] = (0, 0, 0)
    np.write()


def fill(r, g, b):
    for i in range(COUNT):
        np[i] = (r, g, b)
    np.write()


def set_pixel(grid_idx, r, g, b):
    if 0 <= grid_idx < COUNT:
        np[LOOKUP[grid_idx]] = (r, g, b)


def stop_animation():
    state["fn"] = None
    state["name"] = "off"
    state["custom_code"] = ""


def start_preset(name, persist=True):
    if name == "off":
        stop_animation()
        clear()
        state["error"] = ""
        if persist: save_active()
        return True, ""
    cls = presets.PRESETS.get(name)
    if cls is None:
        return False, "unknown preset: " + name
    try:
        inst = cls()
    except Exception as e:
        state["error"] = "init: " + repr(e)
        return False, state["error"]
    clear()
    state["fn"] = inst.step
    state["name"] = name
    state["frame"] = 0
    state["error"] = ""
    state["custom_code"] = ""
    if persist: save_active()
    return True, ""


def install_custom(code, persist=True):
    ns = {
        "math": math,
        "random": random,
        "time": time,
        "COUNT": COUNT,
    }
    try:
        exec(code, ns)
    except Exception as e:
        state["error"] = "compile: " + repr(e)
        return False, state["error"]
    fn = ns.get("step")
    if not callable(fn):
        state["error"] = "code must define `def step(frame, np, LOOKUP):`"
        return False, state["error"]
    clear()
    state["fn"] = fn
    state["name"] = "custom"
    state["frame"] = 0
    state["error"] = ""
    state["custom_code"] = code
    if persist: save_active()
    return True, ""


HTML = b"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Pixels64</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{margin:0;background:#111;color:#eee;font-family:-apple-system,sans-serif;padding:14px;user-select:none;-webkit-user-select:none}
h1{margin:0 0 12px;font-size:16px;letter-spacing:2px;text-align:center}
.layout{display:flex;gap:18px;justify-content:center;align-items:flex-start;max-width:900px;margin:0 auto}
.left{display:flex;flex-direction:column;gap:5px;width:170px;flex-shrink:0}
#preset-buttons{display:flex;flex-direction:column;gap:5px}
#preset-buttons button{width:100%;box-sizing:border-box}
.left>button{width:100%;box-sizing:border-box}
.left .hdr{font-size:11px;color:#666;letter-spacing:1px;margin:6px 0 2px;text-transform:uppercase}
.right{display:flex;flex-direction:column;align-items:center;gap:14px;flex:1;min-width:0}
.row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:center}
.slider-row{display:flex;gap:8px;align-items:center}
.slider-row input[type=range]{flex:1}
button{padding:8px 12px;background:#222;color:#eee;border:1px solid #444;border-radius:6px;font-size:13px;cursor:pointer;font-family:inherit;text-align:left}
button:active{background:#333}
button.active{background:#2a5a3a;border-color:#4a8a5a}
input[type=color]{width:44px;height:36px;border:1px solid #444;background:#222;border-radius:6px;cursor:pointer;padding:0}
#grid{display:grid;grid-template-columns:repeat(8,38px);grid-template-rows:repeat(8,38px);gap:3px;background:#000;padding:6px;border-radius:8px;touch-action:none}
.cell{background:#000;border:1px solid #222;border-radius:4px;cursor:pointer}
#status{font-size:12px;color:#888;min-height:16px;text-align:center}
#err{font-size:12px;color:#e66;min-height:16px;text-align:center;max-width:400px;word-break:break-word}
textarea{width:100%;max-width:420px;height:180px;background:#0a0a0a;color:#eee;border:1px solid #333;border-radius:6px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;padding:8px;resize:vertical;-webkit-user-select:text;user-select:text;box-sizing:border-box}
details{width:100%;max-width:420px}
summary{cursor:pointer;font-size:13px;color:#aaa;padding:4px 0}
.sep{width:100%;max-width:420px;height:1px;background:#333;margin:4px 0}
@media(max-width:720px){.layout{flex-direction:column;align-items:center}.left{width:100%;max-width:320px}}
</style></head><body>
<h1>PIXELS64</h1>

<div class="layout">
  <div class="left">
    <div class="hdr">Presets</div>
    <div id="preset-buttons"></div>
    <button id="stop">Stop</button>
  </div>

  <div class="right">
    <div class="row">
      <input type="color" id="pick" value="#ff3030">
      <button id="clr">Clear</button>
      <button id="fil">Fill</button>
    </div>
    <div class="slider-row" style="width:100%;max-width:340px">
      <span style="font-size:12px;color:#aaa;min-width:54px">FPS <span id="fps-val">8</span></span>
      <input type="range" id="fps" min="1" max="30" step="1" value="8">
    </div>
    <div class="slider-row" style="width:100%;max-width:340px">
      <span style="font-size:12px;color:#aaa;min-width:54px">Bri <span id="bri-val">1.00</span></span>
      <input type="range" id="bri" min="0" max="1" step="0.05" value="1">
    </div>
    <div id="grid"></div>
    <div id="status"></div>
    <div id="err"></div>

    <details>
      <summary>Custom code</summary>
      <textarea id="code" spellcheck="false">import math
def step(frame, np, LOOKUP):
    for i in range(64):
        h = ((i + frame) % 64) / 64
        v = (math.sin(frame * 0.05 + i * 0.1) + 1) / 4
        np[LOOKUP[i]] = (int(60 * v), int(30 * (1 - v)), int(60 * (1 - v)))
</textarea>
      <div class="row" style="margin-top:8px"><button id="run">Run custom</button></div>
    </details>
  </div>
</div>

<script>
const grid=document.getElementById('grid');
const pick=document.getElementById('pick');
const status=document.getElementById('status');
const errEl=document.getElementById('err');
const presetWrap=document.getElementById('preset-buttons');
let down=false,pending=new Map(),inflight=false;

function hex2rgb(h){return [parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16)]}

async function flush(){
  if(inflight||pending.size===0)return;
  inflight=true;
  const batch=[...pending.entries()].map(([i,c])=>i+','+c[0]+','+c[1]+','+c[2]).join('\\n');
  pending.clear();
  try{await fetch('/batch',{method:'POST',body:batch})}catch(e){}
  inflight=false;
  if(pending.size>0)flush();
}
function paint(idx,cell){
  const h=pick.value;const [r,g,b]=hex2rgb(h);
  cell.style.background=h;
  pending.set(idx,[r,g,b]);
  flush();
}
function cellAt(x,y){const el=document.elementFromPoint(x,y);return (el&&el.classList.contains('cell'))?el:null}

for(let i=0;i<64;i++){
  const c=document.createElement('div');
  c.className='cell';c.dataset.idx=i;
  c.addEventListener('mousedown',e=>{down=true;paint(i,c);e.preventDefault()});
  c.addEventListener('mouseenter',()=>{if(down)paint(i,c)});
  grid.appendChild(c);
}
document.addEventListener('mouseup',()=>down=false);
document.addEventListener('mouseleave',()=>down=false);
grid.addEventListener('touchstart',e=>{const t=e.touches[0];const c=cellAt(t.clientX,t.clientY);if(c)paint(+c.dataset.idx,c);e.preventDefault()},{passive:false});
grid.addEventListener('touchmove',e=>{const t=e.touches[0];const c=cellAt(t.clientX,t.clientY);if(c)paint(+c.dataset.idx,c);e.preventDefault()},{passive:false});

document.getElementById('clr').onclick=()=>{
  fetch('/clear',{method:'POST'});
  document.querySelectorAll('.cell').forEach(c=>c.style.background='#000');
};
document.getElementById('fil').onclick=()=>{
  const h=pick.value;const [r,g,b]=hex2rgb(h);
  fetch('/fill',{method:'POST',body:r+','+g+','+b});
  document.querySelectorAll('.cell').forEach(c=>c.style.background=h);
};
document.getElementById('stop').onclick=async()=>{
  await fetch('/preset',{method:'POST',body:'off'});
  refreshState();
};
document.getElementById('run').onclick=async()=>{
  errEl.textContent='';
  const r=await fetch('/custom',{method:'POST',body:document.getElementById('code').value});
  const txt=await r.text();
  if(!r.ok)errEl.textContent=txt;
  refreshState();
};

let knownPresets=null;
function buildPresetButtons(names){
  presetWrap.innerHTML='';
  names.forEach(n=>{
    const b=document.createElement('button');
    b.textContent=n;b.dataset.name=n;
    b.onclick=async()=>{await fetch('/preset',{method:'POST',body:n});refreshState()};
    presetWrap.appendChild(b);
  });
  knownPresets=names.join(',');
}
function markActive(name){
  document.querySelectorAll('#preset-buttons button').forEach(b=>{
    b.classList.toggle('active',b.dataset.name===name);
  });
}
const fpsSlider=document.getElementById('fps');
const fpsVal=document.getElementById('fps-val');
let fpsLockUntil=0;
fpsSlider.addEventListener('input',()=>{fpsVal.textContent=fpsSlider.value});
fpsSlider.addEventListener('change',async()=>{
  fpsLockUntil=Date.now()+2500;
  await fetch('/fps',{method:'POST',body:fpsSlider.value});
});

const briSlider=document.getElementById('bri');
const briVal=document.getElementById('bri-val');
let briLockUntil=0;
function fmtBri(v){return Number(v).toFixed(2)}
briSlider.addEventListener('input',()=>{briVal.textContent=fmtBri(briSlider.value)});
briSlider.addEventListener('change',async()=>{
  briLockUntil=Date.now()+2500;
  await fetch('/brightness',{method:'POST',body:briSlider.value});
});

async function refreshState(){
  try{
    const r=await fetch('/state');
    const j=await r.json();
    status.textContent='running: '+j.name+' frame='+j.frame+' @ '+j.fps+'fps';
    errEl.textContent=j.error||'';
    const key=j.presets.join(',');
    if(key!==knownPresets)buildPresetButtons(j.presets);
    markActive(j.name);
    if(Date.now()>fpsLockUntil&&String(j.fps)!==fpsSlider.value){
      fpsSlider.value=j.fps;
      fpsVal.textContent=j.fps;
    }
    if(Date.now()>briLockUntil&&fmtBri(j.brightness)!==fmtBri(briSlider.value)){
      briSlider.value=j.brightness;
      briVal.textContent=fmtBri(j.brightness);
    }
  }catch(e){}
}
refreshState();
setInterval(refreshState,5000);
</script></body></html>
"""


def send(cl, status_line, body, ct=b"text/plain"):
    cl.send(
        b"HTTP/1.1 " + status_line + b"\r\nContent-Type: " + ct
        + b"\r\nContent-Length: " + str(len(body)).encode()
        + b"\r\nConnection: close\r\n\r\n" + body
    )


def read_req(cl):
    cl.settimeout(3)
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = cl.recv(512)
        if not chunk:
            return None, None, None
        data += chunk
        if len(data) > 32768:
            return None, None, None
    header, _, body = data.partition(b"\r\n\r\n")
    lines = header.split(b"\r\n")
    parts = lines[0].split(b" ")
    if len(parts) < 2:
        return None, None, None
    method, path = parts[0], parts[1]
    clen = 0
    for line in lines[1:]:
        if line.lower().startswith(b"content-length:"):
            try:
                clen = int(line.split(b":", 1)[1].strip())
            except:
                clen = 0
            break
    while len(body) < clen:
        chunk = cl.recv(1024)
        if not chunk:
            break
        body += chunk
    return method, path, body


def handle(cl):
    method, path, body = read_req(cl)
    if method is None:
        return
    mark_activity()
    state["dark"] = False
    if method == b"GET" and path == b"/":
        send(cl, b"200 OK", HTML, b"text/html")
    elif method == b"GET" and path == b"/state":
        payload = {
            "name": state["name"],
            "frame": state["frame"],
            "error": state["error"],
            "fps": 1000 // state["tick_ms"],
            "brightness": np.brightness,
            "presets": list(presets.PRESETS.keys()),
        }
        send(cl, b"200 OK", json.dumps(payload).encode(), b"application/json")
    elif method == b"POST" and path == b"/preset":
        ok, msg = start_preset(body.decode().strip())
        send(cl, b"200 OK" if ok else b"400 Bad Request", msg.encode() or b"ok")
    elif method == b"POST" and path == b"/custom":
        ok, msg = install_custom(body.decode())
        send(cl, b"200 OK" if ok else b"400 Bad Request", msg.encode() or b"ok")
    elif method == b"POST" and path == b"/fps":
        try:
            fps = int(body.decode().strip())
            if fps < 1: fps = 1
            if fps > 30: fps = 30
            state["tick_ms"] = 1000 // fps
            send(cl, b"200 OK", b"ok")
        except Exception as e:
            send(cl, b"400 Bad Request", str(e).encode())
    elif method == b"POST" and path == b"/brightness":
        try:
            b = float(body.decode().strip())
            if b < 0: b = 0.0
            if b > 1: b = 1.0
            np.brightness = b
            np.write()
            send(cl, b"200 OK", b"ok")
        except Exception as e:
            send(cl, b"400 Bad Request", str(e).encode())
    elif method == b"POST" and path == b"/batch":
        stop_animation()
        for line in body.split(b"\n"):
            line = line.strip()
            if not line:
                continue
            try:
                p = line.split(b",")
                set_pixel(int(p[0]), int(p[1]), int(p[2]), int(p[3]))
            except:
                pass
        np.write()
        send(cl, b"200 OK", b"ok")
    elif method == b"POST" and path == b"/pixel":
        stop_animation()
        try:
            idx, r, g, bl = (int(x) for x in body.split(b","))
            set_pixel(idx, r, g, bl)
            np.write()
            send(cl, b"200 OK", b"ok")
        except Exception as e:
            send(cl, b"400 Bad Request", str(e).encode())
    elif method == b"POST" and path == b"/fill":
        stop_animation()
        try:
            r, g, bl = (int(x) for x in body.split(b","))
            fill(r, g, bl)
            send(cl, b"200 OK", b"ok")
        except Exception as e:
            send(cl, b"400 Bad Request", str(e).encode())
    elif method == b"POST" and path == b"/clear":
        stop_animation()
        clear()
        send(cl, b"200 OK", b"ok")
    elif method == b"GET" and path == b"/ping":
        send(cl, b"200 OK", b"pong\n")
    else:
        send(cl, b"404 Not Found", b"nope")


clear()

saved = load_active()
if saved:
    try:
        if saved.get("name") == "custom" and saved.get("code"):
            install_custom(saved["code"], persist=False)
        elif saved.get("name") and saved["name"] != "off":
            start_preset(saved["name"], persist=False)
    except Exception as e:
        print("restore err:", e)

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
srv = socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(addr)
srv.listen(2)
srv.setblocking(False)

poller = select.poll()
poller.register(srv, select.POLLIN)

print("SERVER_LISTENING", addr)

while True:
    if state["fn"] and not state["dark"]:
        elapsed = time.ticks_diff(time.ticks_ms(), state["last_tick"])
        poll_ms = max(0, min(20, state["tick_ms"] - elapsed))
    else:
        poll_ms = 200

    for _ in poller.poll(poll_ms):
        try:
            cl, ca = srv.accept()
        except OSError:
            continue
        try:
            handle(cl)
        except Exception as e:
            print("ERR", e)
        finally:
            try:
                cl.close()
            except:
                pass
        gc.collect()

    if not state["dark"] and time.ticks_diff(time.ticks_ms(), state["last_activity"]) > IDLE_MS:
        state["dark"] = True
        clear()

    if state["fn"] and not state["dark"]:
        now = time.ticks_ms()
        if time.ticks_diff(now, state["last_tick"]) >= state["tick_ms"]:
            try:
                state["fn"](state["frame"], np, LOOKUP)
                np.write()
                state["frame"] += 1
                state["last_tick"] = now
            except Exception as e:
                state["fn"] = None
                state["name"] = "off"
                state["error"] = "run: " + repr(e)
                print("animate err:", e)
                clear()
            gc.collect()
