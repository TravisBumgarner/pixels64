import random
import time

import machine
import neopixel
from config import LOOKUP

NEO_PIXEL_PIN = 13
NEO_PIXEL_COUNT = 16

neo_pin = machine.Pin(NEO_PIXEL_PIN, machine.Pin.OUT)
np = neopixel.NeoPixel(neo_pin, NEO_PIXEL_COUNT)


GRID_SIDE = 8

PALETTES = [
    ["#949088", "#34373b", "#d5d7d5", "#1179aa", "#c89a00", "#8f1c27"],
    ["#6f6e6d", "#387286", "#434c4e", "#c0b7ae", "#232528", "#969492"],
    ["#e7711c", "#c9beae", "#5595b2", "#dbe2d9", "#5d5d60", "#251c1b"],
    ["#5ab4e2", "#6d6d6e", "#252f32", "#aea79c", "#b28e53", "#2c7878"],
    ["#5d1f1b", "#594a43", "#8c8886", "#432522", "#87624d", "#130e0c"],
    ["#acfbfe", "#c39417", "#98948e", "#2d3344", "#61747f", "#d0c7ba"],
    ["#ac5320", "#e2eef7", "#484043", "#2e0d1c", "#417eba", "#979a98"],
    ["#5d5751", "#077975", "#2f3937", "#181111", "#6a553a", "#ccdeeb"],
    ["#d1695a", "#202726", "#aea190", "#9ebbc8", "#7e6960", "#473832"],
    ["#2c3436", "#5f5e7b", "#e1e7ee", "#435f69", "#30454b", "#57898d"],
    ["#6889a8", "#eee6dd", "#332e20", "#e2deb6", "#776d58", "#b4a688"],
    ["#70492c", "#19110d", "#88949e", "#342e2b", "#340e0b", "#534f4d"],
    ["#344b5d", "#e095b9", "#b7afb0", "#2271ca", "#d5cdcf", "#8f8382"],
    ["#b57e74", "#c5b6ae", "#99857f", "#3c3232", "#d1cdd0", "#746966"],
    ["#2d925e", "#b88233", "#797876", "#cac5c2", "#2b2d28", "#864940"],
    ["#7be0eb", "#8d4a55", "#e2bd51", "#1b1e20", "#4e4e49", "#afafaa"],
    ["#dde2ea", "#7e9bb3", "#1e1917", "#acada8", "#bf8c44", "#625f5a"],
    ["#a6b7bf", "#2f3232", "#afd1ea", "#727a7f", "#515353", "#94a3ad"],
    ["#662b30", "#90817e", "#914e4a", "#260b13", "#bdada4", "#ad3870"],
    ["#e6c785", "#899da2", "#384a47", "#d0a353", "#bfc5c8", "#558187"],
    ["#9b3533", "#241b21", "#566b62", "#b3b5a8", "#5b3f3c", "#ddded3"],
    ["#332933", "#f1b0bc", "#a75f8a", "#dbdde1", "#c96590", "#a95f9a"],
    ["#62c795", "#c49647", "#f7939c", "#323f4d", "#e0f9f6", "#94c5c2"],
    ["#566eac", "#693f19", "#221d2f", "#a0a7b0", "#f1b326", "#465685"],
    ["#c2966b", "#6b503d", "#9c6437", "#c8b7a7", "#87705e", "#2f2829"],
    ["#c4c9d3", "#262022", "#815a49", "#b7bbc4", "#aaa096", "#d3d7de"],
    ["#6bb391", "#10412c", "#979795", "#d3d9db", "#6c4234", "#b0554d"],
    ["#a2502e", "#927352", "#dfe3ec", "#32384a", "#d4b64b", "#5d75a2"],
    ["#d3b741", "#98452f", "#e1d7d5", "#3b3027", "#9a8a71", "#635442"],
    ["#4f8a5f", "#e3ab68", "#364146", "#824246", "#b2885d", "#f8e3c0"],
    ["#4bb6be", "#bcafaa", "#9b958e", "#847265", "#b1a39e", "#212125"],
    ["#95606e", "#0c6e82", "#00512b", "#7e563b", "#bdbec1", "#8f3d37"],
    ["#765e7d", "#281411", "#e2e6ea", "#5e160e", "#4f4349", "#6a93a7"],
    ["#959998", "#3b373e", "#c0d1dd", "#1a1818", "#727472", "#76551e"],
    ["#cbb3a0", "#70696a", "#373438", "#a18f85", "#7d7a7e", "#575254"],
    ["#806259", "#a89c8f", "#577385", "#639abb", "#c5b4a1", "#353f48"],
    ["#3c2627", "#b6afaa", "#dbdfe2", "#5c6061", "#d5d1ca", "#9d3335"],
    ["#c58e76", "#fde690", "#8fae8b", "#64543b", "#dfc89c", "#8f7a5b"],
    ["#dbccc2", "#8f4738", "#c48d26", "#344962", "#c3b186", "#987c58"],
    ["#98c0b0", "#413c39", "#f0e6d6", "#848285", "#bcaba4", "#bbcfc6"],
    ["#5a5453", "#332a20", "#dad5d0", "#b37610", "#610f01", "#075676"],
    ["#d7d0cc", "#926e35", "#414433", "#aa8a50", "#bea794", "#e4b2a7"],
    ["#8798b6", "#827978", "#357878", "#4b2635", "#5c5652", "#6796a8"],
    ["#cca153", "#212221", "#7cb3cc", "#e3dad0", "#2c5252", "#867653"],
    ["#783220", "#bdbfc4", "#205677", "#b8984f", "#9e978d", "#1c2026"],
    ["#abbdcf", "#155480", "#64574f", "#96a9b9", "#7e8485", "#162535"],
    ["#c46f55", "#516066", "#111721", "#c9c8c4", "#3f85b7", "#363d3a"],
    ["#cb8c68", "#5c5b58", "#ddb18b", "#cd8878", "#86827b", "#353637"],
    ["#bebcbc", "#634731", "#88a2b4", "#332111", "#b99482", "#8f3e2f"],
    ["#a37f32", "#65615f", "#a6a5a5", "#342a23", "#8b6826", "#1f5873"],
    ["#4ba4c0", "#58514c", "#c4b9bd", "#a02d55", "#e3e4db", "#27281b"],
    ["#b9ad79", "#997e65", "#8eacc8", "#a18a98", "#86a99b", "#1b1619"],
    ["#909aba", "#dbd8d8", "#3e361e", "#998e85", "#c1b9b8", "#6e6150"],
    ["#353231", "#030c0d", "#62494b", "#686e6f", "#1b1a1a", "#553f3f"],
    ["#cfc1b5", "#69645a", "#98a1b1", "#1b1b24", "#b88e6f", "#f1f3f4"],
    ["#e8c2bf", "#f1da9f", "#ffac80", "#817063", "#fac650", "#ff792b"],
    ["#8cc3c4", "#102422", "#787473", "#454548", "#79b3b4", "#c4bcc9"],
    ["#da9d9c", "#3e3633", "#b67a33", "#7f8d97", "#725d4c", "#be8882"],
    ["#48583b", "#818a74", "#b5bfc9", "#3d3830", "#656956", "#94704c"],
    ["#f0bad1", "#2096ad", "#11100d", "#e0c99e", "#2a7480", "#679eaa"],
    ["#9b1624", "#db9621", "#e7c84f", "#96c28f", "#59b2de", "#9689a7"],
    ["#ae896e", "#718365", "#b16734", "#dcc6b9", "#64462f", "#455177"],
    ["#b89764", "#504842", "#365c8b", "#afada8", "#837263", "#6694ac"],
    ["#a08f82", "#2b5d43", "#f1eceb", "#86c5ba", "#646e5b", "#bdcecb"],
    ["#707077", "#32211a", "#a58f88", "#c0c2c2", "#946d64", "#61504b"],
    ["#846c5a", "#d2d1cf", "#216497", "#8fa1ae", "#323235", "#4d86b2"],
    ["#85888a", "#8a8e92", "#546f63", "#222929", "#7d7f82", "#1b1a19"],
    ["#a7b1a9", "#6d6a65", "#2d2923", "#c1d0c7", "#4e4a43", "#8d908a"],
    ["#a0bca1", "#44281c", "#dddcd4", "#172828", "#9bae96", "#211b19"],
    ["#e9d3ab", "#c0966e", "#34544c", "#3b3a28", "#887362", "#76a18e"],
    ["#b69e75", "#669fb5", "#77797b", "#704b47", "#9d5f5b", "#232828"],
    ["#5c663a", "#98a7ba", "#73808c", "#253431", "#ced9e1", "#0885af"],
    ["#a49a95", "#a7ab9a", "#f4f5f6", "#3c312c", "#a57163", "#ccc8bb"],
    ["#262928", "#8f9376", "#9d5935", "#5f5e48", "#0877b3", "#cf9240"],
    ["#c27b69", "#9dafb9", "#3768b3", "#1a1f25", "#5c5f68", "#2d3b4a"],
    ["#e9dc87", "#cfb789", "#222b32", "#cdd5d7", "#a7938a", "#478b68"],
    ["#d1c8ba", "#47473d", "#17191b", "#b6a413", "#b68586", "#0c80a8"],
    ["#c6b7bc", "#372a2b", "#6c5052", "#b79baa", "#d6cbcf", "#90777c"],
    ["#ceaf6a", "#33221b", "#d2d4d5", "#637361", "#b8b5a9", "#8a9886"],
    ["#5a996f", "#e8ce94", "#2d2b29", "#81786f", "#bc8c69", "#e9eaea"],
    ["#94b8c2", "#4e5d5b", "#9e897d", "#161a19", "#bb7e1e", "#67929a"],
    ["#97482d", "#ded9d6", "#bb603c", "#435960", "#6a8e98", "#ecbc85"],
    ["#e3a5ac", "#0eb2ec", "#eeebe8", "#c8a76b", "#5b6976", "#93888e"],
    ["#eee1cd", "#e8dddc", "#db8979", "#413528", "#b1452d", "#cbb9ac"],
    ["#7f8671", "#47503e", "#d3ccc6", "#6b6c57", "#cda597", "#aa6835"],
    ["#7b8da5", "#5d0b15", "#76705f", "#1c1b21", "#3c7b9b", "#996920"],
    ["#dfe0d9", "#e8c58e", "#292620", "#378d9c", "#575a53", "#b6b3a9"],
    ["#4c7d96", "#153140", "#474a3b", "#1f221d", "#f6cb75", "#c44840"],
    ["#7e6231", "#33436c", "#675948", "#491d0d", "#514439", "#8d8b86"],
    ["#f8b641", "#584f50", "#2a2727", "#c2bebc", "#a07066", "#ad4d44"],
    ["#b0b8c2", "#38434e", "#718191", "#949ca5", "#556474", "#1a1e23"],
    ["#c4cdd6", "#816b5f", "#ca7c52", "#3f6067", "#a19a97", "#002e72"],
    ["#4e2d3d", "#cda897", "#7fb0a1", "#696569", "#e5dcd8", "#a98572"],
    ["#6e353e", "#444250", "#2b2525", "#93979d", "#3a3234", "#5b5b5e"],
    ["#d9e0e4", "#61696b", "#50a2c4", "#422627", "#da9344", "#b23364"],
    ["#a7b590", "#84563d", "#37332f", "#eae5da", "#696d66", "#fbf9f6"],
    ["#d48a95", "#bbc9d4", "#97abb2", "#dbd2d0", "#a79b95", "#332912"],
    ["#221a1a", "#9d9f92", "#dbdbcb", "#6b6a69", "#4f4a4a", "#372d29"],
    ["#b4b7b8", "#e56a52", "#f7f7f6", "#251e1c", "#9c8c7f", "#10204b"],
    ["#0b131a", "#4b3e3c", "#23313b", "#62524e", "#2f414c", "#16222b"],
    ["#901000", "#d4cfcd", "#c4982d", "#8e8983", "#33480c", "#5e7418"],
    ["#2b282e", "#01569f", "#d0dae1", "#d7c005", "#da3556", "#4d5b66"],
    ["#2d4238", "#657f7c", "#e0a840", "#049b8e", "#9a9998", "#ad8239"],
    ["#625352", "#a07354", "#dcd4c8", "#4b6680", "#3b3339", "#4c4248"],
    ["#22171c", "#c8b9a9", "#b356cd", "#fa9831", "#34363d", "#0d86aa"],
    ["#058299", "#405564", "#d1840d", "#202821", "#9cc3ed", "#ff6132"],
    ["#2a6472", "#afaeab", "#bf7f3e", "#5595b8", "#7e7d73", "#d9dfe7"],
    ["#466f5f", "#296a97", "#8d807f", "#325542", "#757477", "#695e54"],
    ["#7b6756", "#b3a897", "#d6cfbf", "#212d1b", "#574c3a", "#938678"],
    ["#b15242", "#e1e0db", "#9a3421", "#1b1010", "#e9dc4e", "#3a51a8"],
    ["#65cda7", "#97ddd1", "#d67684", "#edb9aa", "#577491", "#cca738"],
    ["#b5974c", "#dbb8b4", "#99bbae", "#384b43", "#443c32", "#aba89d"],
    ["#0e4d79", "#7a5b36", "#dceaf3", "#465c61", "#959899", "#2c3637"],
    ["#805543", "#922b24", "#c59187", "#de8c4c", "#b3a194", "#653729"],
    ["#6a1511", "#688791", "#f4763c", "#d4d5d1", "#42525b", "#558d7f"],
    ["#4d6b4e", "#c3a798", "#ded0c5", "#b17c6e", "#7b9071", "#283c39"],
    ["#af9e88", "#867b6f", "#272420", "#d2bea1", "#ce7b23", "#af3e47"],
    ["#71bdcf", "#b44d2a", "#fcc735", "#0d1d20", "#ffdb89", "#3f3838"],
    ["#aa947b", "#677575", "#507270", "#59595a", "#868982", "#999c96"],
    ["#9f2d22", "#15508f", "#2a2227", "#777b7d", "#693e2d", "#e1c28f"],
    ["#5a5b5d", "#19191c", "#7fa6c9", "#aaa9ab", "#7298bb", "#6489ab"],
    ["#ac6b5c", "#bdd5e7", "#764c3f", "#757b89", "#fbffff", "#5b2423"],
    ["#e7e7e5", "#bdd230", "#5aa1da", "#808571", "#15181f", "#d36450"],
    ["#a06e36", "#d2c6c0", "#698d85", "#48504f", "#f9f9f9", "#b88b54"],
    ["#f4c26a", "#01325e", "#662b1b", "#0188cb", "#8f604b", "#e58c68"],
    ["#162067", "#bfa7a0", "#e0e9f3", "#b3554f", "#7a7d5a", "#514f35"],
    ["#5c585c", "#f1f2f4", "#b0aba9", "#d5d4d5", "#262126", "#968f8f"],
    ["#8a6030", "#22221a", "#a57436", "#bbaa89", "#444239", "#0c0d09"],
    ["#c3c5bc", "#515855", "#5a9389", "#936d41", "#dae3e0", "#a58868"],
    ["#f09a52", "#ff9cdd", "#2f3335", "#ddd8dc", "#5bafc0", "#ad9aa3"],
    ["#27272f", "#d9d5d5", "#d2c15b", "#1d6d9e", "#89857c", "#c26b60"],
    ["#323c38", "#beb8ad", "#b9a16f", "#7c7d80", "#685c42", "#e0dbcb"],
    ["#6b6a46", "#9e9663", "#b3b9a2", "#1e8096", "#4f7f42", "#e4e4de"],
    ["#030202", "#564815", "#0e0904", "#1e2808", "#0f141b", "#3a3510"],
    ["#f09d6c", "#33282b", "#085497", "#e6e0ce", "#65423a", "#f3f3ef"],
    ["#7f5e78", "#ac9994", "#cad4dc", "#1b1a20", "#00827a", "#79a6e1"],
    ["#9a4d49", "#b3ccb5", "#a39a89", "#2a2624", "#4e544c", "#8bb1d1"],
    ["#3e39b6", "#eef2f5", "#335e98", "#1d1e1f", "#b44081", "#35bdc8"],
    ["#c74a38", "#f5aea2", "#d6dcd8", "#1c2630", "#637e89", "#872e2b"],
    ["#e9d9ba", "#697c87", "#1d2224", "#98a5a9", "#354953", "#c2cccd"],
    ["#bb860c", "#c9baa2", "#f0e4dc", "#9c8870", "#1f293a", "#26715d"],
    ["#a84e3e", "#523a2f", "#e5b64f", "#0c2536", "#8d6933", "#b39159"],
    ["#cadaeb", "#5c6568", "#4ea8a1", "#363a3d", "#9db9d0", "#8e6a29"],
    ["#144e7d", "#bd955a", "#358dc0", "#2f2f2d", "#7d767a", "#3d6485"],
    ["#a3200c", "#b4b3b1", "#7aaac8", "#2a231a", "#58524f", "#7e93a0"],
]


def generate_cluster_origins(origin_count):
    # Create all points in the grid (excluding edges)
    all_points = []
    for x in range(1, GRID_SIDE - 1):
        for y in range(1, GRID_SIDE - 1):
            all_points.append((x, y))

    # Shuffle the points
    shuffle_array(all_points)

    # Selected points to return
    selected_points = []

    # For each point, check if it's valid (not near edges of already selected points)
    for point in all_points:
        if len(selected_points) >= origin_count:
            break

        # Check if this point is valid (not near any already selected point)
        is_valid = True
        for selected in selected_points:
            # If point is adjacent to or diagonal to a selected point, it's invalid
            if abs(point[0] - selected[0]) <= 1 and abs(point[1] - selected[1]) <= 1:
                is_valid = False
                break

        if is_valid:
            selected_points.append(point)
    return selected_points


DIRECTIONS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]


def is_point_in_grid(point):
    return (
        0 <= point[0] < GRID_SIDE
        and 0 <= point[1] < GRID_SIDE
        and point[0] >= 0
        and point[1] >= 0
    )


def is_point_free(grid, point):
    return grid[point[0]][point[1]] == -1


def is_point_available(grid, point):
    return is_point_in_grid(point) and is_point_free(grid, point)


# Returns the number of valid points needed to fill the cluster in the given direction.
def get_number_of_valid_points_needed(cluster, direction):
    cluster_width = (
        1 + max(point[0] for point in cluster) - min(point[0] for point in cluster)
    )
    cluster_height = (
        1 + max(point[1] for point in cluster) - min(point[1] for point in cluster)
    )

    if direction == (0, 1):
        return cluster_width
    elif direction == (1, 0):
        return cluster_height
    elif direction == (0, -1):
        return cluster_width
    elif direction == (-1, 0):
        return cluster_height


# Doesn't currently support leaving a gap.
def get_valid_points_for_direction(grid, cluster, direction):
    valid_points = []
    for point in cluster:
        new_point = (point[0] + direction[0], point[1] + direction[1])
        if is_point_available(grid, new_point):
            valid_points.append(new_point)
    return valid_points


def build_color_grid(PALETTE):
    grid = [[-1 for _ in range(GRID_SIDE)] for _ in range(GRID_SIDE)]
    origins = generate_cluster_origins(len(PALETTE))

    clusters = [[origin] for origin in origins]

    for i, origin in enumerate(origins):
        grid[origin[0]][origin[1]] = i

    can_expand = [True for _ in PALETTE]

    while any(can_expand):
        for i, cluster in enumerate(clusters):
            if not can_expand[i]:
                continue

            has_expanded = False

            for direction in DIRECTIONS:

                valid_points = get_valid_points_for_direction(grid, cluster, direction)

                if len(valid_points) == get_number_of_valid_points_needed(
                    cluster, direction
                ):
                    for point in valid_points:
                        grid[point[0]][point[1]] = i
                        cluster.append(point)
                    has_expanded = True
                    break

            if not has_expanded:
                can_expand[i] = False

    for row in grid:
        print(row)

    return grid


def shuffle_array(arr):
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def display_color_palettes():
    while True:
        # Use random palette index instead of sequential
        palette_index = random.randint(0, len(PALETTES) - 1)
        rgb_palette = [hex_to_rgb(color) for color in PALETTES[palette_index]]
        grid = build_color_grid(rgb_palette)

        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                lookup_index = LOOKUP[i * GRID_SIDE + j]
                np[lookup_index] = rgb_palette[value]
        np.write()

        time.sleep(60 * 1)


# Currently doing just one display
all_displays = {
    "color_palettes": display_color_palettes,
}

if __name__ == "__main__":
    display_color_palettes()
