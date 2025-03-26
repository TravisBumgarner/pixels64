from config import LOOKUP


def display_all_yellow(strip):
    for i in range(len(LOOKUP)):
        strip[LOOKUP[i]] = (255, 255, 0)
    strip.write()


def display_all_green(strip):
    for i in range(len):
        strip[LOOKUP[i]] = (0, 255, 0)
    strip.write()


def display_all_blue(strip):
    for i in range(len):
        strip[LOOKUP[i]] = (0, 0, 255)
    strip.write()
