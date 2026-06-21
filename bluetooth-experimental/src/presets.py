import math
import random

SIZE = 8
COUNT = 64


def _hsv(h, s, v):
    i = int(h * 6) % 6
    f = h * 6 - int(h * 6)
    p = int(255 * v * (1 - s))
    q = int(255 * v * (1 - f * s))
    t = int(255 * v * (1 - (1 - f) * s))
    vv = int(255 * v)
    if i == 0: return (vv, t, p)
    if i == 1: return (q, vv, p)
    if i == 2: return (p, vv, t)
    if i == 3: return (p, q, vv)
    if i == 4: return (t, p, vv)
    return (vv, p, q)


def _idx(LOOKUP, row, col):
    return LOOKUP[row * SIZE + col]


def _rand_color(lo=0, hi=200):
    return (random.randint(lo, hi), random.randint(lo, hi), random.randint(lo, hi))


def _lerp(c1, c2, f):
    return (
        int(c1[0] + (c2[0] - c1[0]) * f),
        int(c1[1] + (c2[1] - c1[1]) * f),
        int(c1[2] + (c2[2] - c1[2]) * f),
    )


def _fade_all(np, LOOKUP, f):
    for i in range(COUNT):
        idx = LOOKUP[i]
        r, g, b = np[idx]
        np[idx] = (int(r * f), int(g * f), int(b * f))


class Rainbow:
    def step(self, frame, np, LOOKUP):
        for i in range(COUNT):
            h = ((i + frame) % COUNT) / COUNT
            np[LOOKUP[i]] = _hsv(h, 1, 0.25)


class Chase:
    def step(self, frame, np, LOOKUP):
        for i in range(COUNT):
            np[LOOKUP[i]] = (0, 0, 0)
        np[LOOKUP[frame % COUNT]] = (60, 60, 60)


class Pulse:
    def step(self, frame, np, LOOKUP):
        v = (math.sin(frame * 0.1) + 1) / 2
        c = (int(60 * v), 0, int(60 * (1 - v)))
        for i in range(COUNT):
            np[LOOKUP[i]] = c


class Sparkle:
    def step(self, frame, np, LOOKUP):
        for i in range(COUNT):
            idx = LOOKUP[i]
            r, g, b = np[idx]
            np[idx] = (max(0, r - 4), max(0, g - 4), max(0, b - 4))
        for _ in range(2):
            np[LOOKUP[random.randint(0, 63)]] = (80, 80, 80)


class Plasma:
    def step(self, frame, np, LOOKUP):
        t = frame * 0.06
        for y in range(SIZE):
            for x in range(SIZE):
                v = math.sin(x * 0.6 + t) + math.sin(y * 0.6 + t * 1.3) + math.sin((x + y) * 0.4 + t * 0.7)
                h = (v + 3) / 6
                np[_idx(LOOKUP, y, x)] = _hsv(h, 1, 0.2)


class RandomPulses:
    def __init__(self):
        self.target = {}
        self.start = {}
        self.t0 = {}
        self.steps = 6
        self.fresh = True

    def step(self, frame, np, LOOKUP):
        if self.fresh:
            for i in range(COUNT):
                np[LOOKUP[i]] = _rand_color(20, 200)
            self.fresh = False
            return
        if not self.target or frame % 2 == 0:
            i = random.randint(0, COUNT - 1)
            self.start[i] = np[LOOKUP[i]]
            self.target[i] = _rand_color(20, 220)
            self.t0[i] = frame
        for i in list(self.target):
            t = (frame - self.t0[i]) / self.steps
            if t >= 1:
                np[LOOKUP[i]] = self.target[i]
                del self.target[i]; del self.start[i]; del self.t0[i]
            else:
                np[LOOKUP[i]] = _lerp(self.start[i], self.target[i], t)


class RandomPulsesTowardsColor:
    def __init__(self):
        self.target_color = _rand_color(40, 220)
        self.fresh = True
        self.changes_per_cycle = 32
        self.changes_done = 0

    def step(self, frame, np, LOOKUP):
        if self.fresh:
            for i in range(COUNT):
                np[LOOKUP[i]] = _rand_color(0, 220)
            self.fresh = False
            return
        for _ in range(2):
            i = random.randint(0, COUNT - 1)
            cur = np[LOOKUP[i]]
            np[LOOKUP[i]] = _lerp(cur, self.target_color, 0.7)
            self.changes_done += 1
        if self.changes_done >= self.changes_per_cycle:
            self.changes_done = 0
            self.target_color = _rand_color(40, 220)


class Zigzag:
    def __init__(self):
        self.path = []
        for y in range(SIZE):
            xs = range(SIZE) if y % 2 == 0 else range(SIZE - 1, -1, -1)
            for x in xs:
                self.path.append((x, y))
        self.pos = 0
        self.current = _rand_color(20, 220)
        self.target = _rand_color(20, 220)
        self.sub = 0
        self.sub_max = 40

    def step(self, frame, np, LOOKUP):
        f = self.sub / max(1, self.sub_max - 1)
        color = _lerp(self.current, self.target, f)
        x, y = self.path[self.pos]
        np[_idx(LOOKUP, y, x)] = color
        self.pos = (self.pos + 1) % len(self.path)
        self.sub += 1
        if self.sub >= self.sub_max:
            self.current = self.target
            self.target = _rand_color(20, 220)
            self.sub = 0


class ChristmasSquares:
    PALETTE = [
        (200, 30, 30), (170, 20, 20), (140, 10, 10), (110, 5, 5),
        (30, 200, 30), (20, 150, 20), (10, 110, 10), (5, 80, 5),
        (255, 255, 255), (235, 235, 235),
        (200, 200, 200), (170, 170, 170),
    ]
    SQUARE_SIZE = 2

    def __init__(self):
        self.origins = [(i, j) for i in range(0, SIZE, self.SQUARE_SIZE) for j in range(0, SIZE, self.SQUARE_SIZE)]
        self.last = []
        self.cur_sq = None
        self.cur_color = (0, 0, 0)
        self.tgt_color = (0, 0, 0)
        self.sub = 0
        self.sub_max = 8
        self.fresh = True

    def _fill_sq(self, np, LOOKUP, x, y, color):
        for i in range(self.SQUARE_SIZE):
            for j in range(self.SQUARE_SIZE):
                np[_idx(LOOKUP, y + i, x + j)] = color

    def _next_sq(self):
        avail = [sq for sq in self.origins if sq not in self.last]
        if not avail:
            self.last.pop(0)
            avail = self.origins
        nxt = random.choice(avail)
        self.last.append(nxt)
        if len(self.last) > 3:
            self.last.pop(0)
        return nxt

    def step(self, frame, np, LOOKUP):
        if self.fresh:
            for x, y in self.origins:
                self._fill_sq(np, LOOKUP, x, y, random.choice(self.PALETTE))
            self.fresh = False
            x, y = self._next_sq()
            self.cur_sq = (x, y)
            self.cur_color = np[_idx(LOOKUP, y, x)]
            self.tgt_color = random.choice(self.PALETTE)
            self.sub = 0
            return
        x, y = self.cur_sq
        f = self.sub / max(1, self.sub_max - 1)
        self._fill_sq(np, LOOKUP, x, y, _lerp(self.cur_color, self.tgt_color, f))
        self.sub += 1
        if self.sub >= self.sub_max:
            x, y = self._next_sq()
            self.cur_sq = (x, y)
            self.cur_color = np[_idx(LOOKUP, y, x)]
            self.tgt_color = random.choice(self.PALETTE)
            self.sub = 0


class GradientSquares(ChristmasSquares):
    PALETTE = None

    def step(self, frame, np, LOOKUP):
        if self.fresh:
            for x, y in self.origins:
                self._fill_sq(np, LOOKUP, x, y, _rand_color(20, 220))
            self.fresh = False
            x, y = self._next_sq()
            self.cur_sq = (x, y)
            self.cur_color = np[_idx(LOOKUP, y, x)]
            self.tgt_color = _rand_color(20, 220)
            self.sub = 0
            return
        x, y = self.cur_sq
        f = self.sub / max(1, self.sub_max - 1)
        self._fill_sq(np, LOOKUP, x, y, _lerp(self.cur_color, self.tgt_color, f))
        self.sub += 1
        if self.sub >= self.sub_max:
            x, y = self._next_sq()
            self.cur_sq = (x, y)
            self.cur_color = np[_idx(LOOKUP, y, x)]
            self.tgt_color = _rand_color(20, 220)
            self.sub = 0


class DualChase:
    def __init__(self):
        self.path_h = []
        for y in range(SIZE):
            xs = range(SIZE) if y % 2 == 0 else range(SIZE - 1, -1, -1)
            for x in xs:
                self.path_h.append((x, y))
        self.path_v = []
        for x in range(SIZE):
            ys = range(SIZE) if x % 2 == 0 else range(SIZE - 1, -1, -1)
            for y in ys:
                self.path_v.append((x, y))
        self.n = len(self.path_h)
        self.a = 0
        self.b = self.n // 2
        self.h = random.random()
        self.horizontal = True
        self.steps = 0

    def step(self, frame, np, LOOKUP):
        _fade_all(np, LOOKUP, 0.92)
        path = self.path_h if self.horizontal else self.path_v
        x1, y1 = path[self.a]
        x2, y2 = path[self.b]
        c1 = _hsv(self.h % 1.0, 0.8, 0.4)
        c2 = _hsv((self.h + 0.5) % 1.0, 0.8, 0.4)
        np[_idx(LOOKUP, y1, x1)] = c1
        np[_idx(LOOKUP, y2, x2)] = c2
        self.a = (self.a + 1) % self.n
        self.b = (self.b + 1) % self.n
        self.h = (self.h + 0.003) % 1.0
        self.steps += 1
        if self.steps >= self.n:
            self.horizontal = not self.horizontal
            self.steps = 0


def _hilbert_d2xy(n, d):
    x = y = 0
    s = 1
    t = d
    while s < n:
        rx = 1 & (t // 2)
        ry = 1 & (t ^ rx)
        if ry == 0:
            if rx == 1:
                x = s - 1 - x
                y = s - 1 - y
            x, y = y, x
        x += s * rx
        y += s * ry
        t //= 4
        s *= 2
    return x, y


class HilbertWave:
    def __init__(self):
        self.path = [_hilbert_d2xy(SIZE, i) for i in range(COUNT)]
        self.k = 0
        self.base = random.random()

    def step(self, frame, np, LOOKUP):
        _fade_all(np, LOOKUP, 0.92)
        for i in range(SIZE // 2):
            x, y = self.path[(self.k - i) % len(self.path)]
            color = _hsv((self.base + i * 0.02) % 1.0, 0.7, 0.35 * (1 - i / (SIZE // 2)))
            p = _idx(LOOKUP, y, x)
            r0, g0, b0 = np[p]
            r1, g1, b1 = color
            np[p] = (min(255, r0 + r1), min(255, g0 + g1), min(255, b0 + b1))
        self.k = (self.k + 1) % len(self.path)
        self.base = (self.base + 0.002) % 1.0


class MortonWeave:
    def __init__(self):
        def d2xy(d):
            x = ((d >> 0) & 1) | (((d >> 2) & 1) << 1) | (((d >> 4) & 1) << 2)
            y = ((d >> 1) & 1) | (((d >> 3) & 1) << 1) | (((d >> 5) & 1) << 2)
            return x, y
        self.path = [d2xy(i) for i in range(COUNT)]
        self.k = 0
        self.hue = random.random()

    def step(self, frame, np, LOOKUP):
        _fade_all(np, LOOKUP, 0.90)
        for i in range(6):
            x, y = self.path[(self.k + i * 3) % len(self.path)]
            idx = _idx(LOOKUP, y, x)
            col = _hsv((self.hue + i * 0.08) % 1.0, 0.7, 0.32)
            r, g, b = np[idx]
            rr, gg, bb = col
            np[idx] = (min(255, r + rr), min(255, g + gg), min(255, b + bb))
        self.k = (self.k + 1) % len(self.path)
        self.hue = (self.hue + 0.002) % 1.0


class SpiralScan:
    def __init__(self):
        order = []
        x = y = SIZE // 2
        dx, dy = 1, 0
        step_len = 1
        order.append((x, y))
        while len(order) < COUNT:
            for _ in range(step_len):
                x += dx
                y += dy
                if 0 <= x < SIZE and 0 <= y < SIZE:
                    order.append((x, y))
                if len(order) >= COUNT:
                    break
            dx, dy = -dy, dx
            if dy == 0:
                step_len += 1
        self.order = order
        self.k = 0
        self.base = random.random()

    def step(self, frame, np, LOOKUP):
        n = len(self.order)
        for i, (x, y) in enumerate(self.order):
            frac = ((i + self.k) % n) / (n - 1)
            h = (self.base + 0.25 * frac) % 1.0
            v = 0.12 + 0.22 * (1 - abs(0.5 - frac) * 2)
            np[_idx(LOOKUP, y, x)] = _hsv(h, 0.45, v)
        self.base = (self.base + 0.002) % 1.0
        self.k = (self.k + 1) % n


class JpegZigzag:
    def __init__(self):
        order = []
        for s in range(0, 2 * SIZE - 1):
            if s % 2 == 0:
                x = min(s, SIZE - 1)
                y = s - x
                while x >= 0 and y < SIZE:
                    order.append((x, y))
                    x -= 1
                    y += 1
            else:
                y = min(s, SIZE - 1)
                x = s - y
                while y >= 0 and x < SIZE:
                    order.append((x, y))
                    y -= 1
                    x += 1
        self.order = order
        self.k = 0
        self.hue = random.random()

    def step(self, frame, np, LOOKUP):
        _fade_all(np, LOOKUP, 0.94)
        for i in range(5):
            x, y = self.order[(self.k + i * 2) % len(self.order)]
            idx = _idx(LOOKUP, y, x)
            col = _hsv((self.hue + i * 0.06) % 1.0, 0.65, 0.34)
            r, g, b = np[idx]
            rr, gg, bb = col
            np[idx] = (min(255, r + rr), min(255, g + gg), min(255, b + bb))
        self.k = (self.k + 1) % len(self.order)
        self.hue = (self.hue + 0.002) % 1.0


class DiagonalWave:
    def __init__(self):
        self.t = 0.0
        self.base = random.random()

    def step(self, frame, np, LOOKUP):
        self.t += 0.06
        self.base = (self.base + 0.001) % 1.0
        for y in range(SIZE):
            for x in range(SIZE):
                a = math.sin(0.6 * (x + y) + self.t)
                b = math.sin(0.6 * (x - y) - self.t * 0.8)
                w = (a * 0.6 + b * 0.4 + 2) / 4
                np[_idx(LOOKUP, y, x)] = _hsv((self.base + 0.12 * w) % 1.0, 0.55, 0.14 + 0.24 * w)


class VoronoiRipple:
    def __init__(self):
        self.sites = []
        for _ in range(5):
            self.sites.append([
                random.uniform(0, SIZE - 1),
                random.uniform(0, SIZE - 1),
                random.uniform(-0.08, 0.08),
                random.uniform(-0.08, 0.08),
                random.random(),
            ])
        self.t = 0.0

    def step(self, frame, np, LOOKUP):
        self.t += 0.05
        for s in self.sites:
            s[0] = (s[0] + s[2]) % SIZE
            s[1] = (s[1] + s[3]) % SIZE
            s[4] = (s[4] + 0.002) % 1.0
        for y in range(SIZE):
            for x in range(SIZE):
                best = 1e9
                hh = 0.0
                for sx, sy, _, __, h in self.sites:
                    dx = x - sx; dy = y - sy
                    d = (dx * dx + dy * dy) ** 0.5
                    if d < best:
                        best = d
                        hh = h
                w = (math.sin(best * 0.9 - self.t * 0.8) + 1) / 2
                np[_idx(LOOKUP, y, x)] = _hsv((0.55 + 0.2 * hh) % 1.0, 0.55, 0.14 + 0.24 * w)


PRESETS = {
    "rainbow": Rainbow,
    "chase": Chase,
    "pulse": Pulse,
    "sparkle": Sparkle,
    "plasma": Plasma,
    "christmas": ChristmasSquares,
    "gradient_squares": GradientSquares,
    "random_pulses": RandomPulses,
    "pulses_toward": RandomPulsesTowardsColor,
    "zigzag": Zigzag,
    "dual_chase": DualChase,
    "hilbert": HilbertWave,
    "morton": MortonWeave,
    "spiral": SpiralScan,
    "jpeg_zigzag": JpegZigzag,
    "diagonal_wave": DiagonalWave,
    "voronoi": VoronoiRipple,
}
