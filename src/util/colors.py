blue = (0, 0, 128)
black = (0,0,0)
white = (255,255,255)
shadow = (192, 192, 192)
white = (255, 255, 255)
lightGreen = (0, 255, 0)
green = (0, 200, 0)
darkGreen = (0, 100, 0)
yellow = (255,255,0)
blue = (0, 0, 128)
grey = (169, 169, 169)
lightBlue = (0, 0, 255)
cyan = (50, 255, 255)
red = (200, 0, 0)
lightRed = (255, 100, 100)
purple = (102, 0, 102)
orangeRed = (255,69,0)

# Colors from the game palette
slate_blue = (58, 73, 100)
steel_blue = (84, 108, 145)
sky_blue = (109, 156, 190)
pale_cyan = (143, 200, 215)
light_teal1 = (189, 226, 225)
light_teal2 = (189, 226, 225)
light_teal3 = (189, 226, 225)
light_teal4 = (189, 226, 225)
light_teal5 = (189, 226, 225)
deep_forest = (40, 59, 54)
moss_green = (56, 93, 62)
lime_olive = (88, 135, 74)
sage_green = (131, 171, 94)
light_olive = (180, 205, 120)
pale_pear = (218, 223, 172)
pale_pear2 = (218, 223, 172)
pale_pear3 = (218, 223, 172)
pale_pear4 = (218, 223, 172)
pale_pear5 = (218, 223, 172)
maroon_brown = (85, 59, 64)
warm_taupe = (128, 90, 86)
sandy_clay = (180, 137, 114)
rosy_beige = (198, 164, 140)
faded_sand = (221, 198, 174)
parchment = (235, 225, 203)
parchment2 = (235, 225, 203)
parchment3 = (235, 225, 203)
parchment4 = (235, 225, 203)
parchment5 = (235, 225, 203)
dark_plum = (60, 43, 50)
dusty_rose = (103, 63, 63)
terracotta = (141, 93, 69)
amber = (191, 134, 78)
wheat_gold = (219, 173, 101)
muted_camel = (231, 204, 145)
muted_camel2 = (231, 204, 145)
muted_camel3 = (231, 204, 145)
muted_camel4 = (231, 204, 145)
muted_camel5 = (231, 204, 145)
black_purple = (46, 34, 47)
vintage_wine = (72, 46, 60)
crimson_blush = (121, 60, 74)
coral_red = (168, 78, 78)
peach_rose = (207, 115, 96)
apricot = (216, 153, 99)
apricot2 = (216, 153, 99)
apricot3 = (216, 153, 99)
apricot4 = (216, 153, 99)
apricot5 = (216, 153, 99)
dusty_lavender = (45, 44, 65)
plum_grey = (75, 57, 89)
violet_punch = (128, 76, 129)
orchid_purple = (167, 90, 149)
fuchsia_mauve = (201, 112, 166)
blush_pink = (226, 161, 186)
blush_pink2 = (226, 161, 186)
blush_pink3 = (226, 161, 186)
blush_pink4 = (226, 161, 186)
blush_pink5 = (226, 161, 186)
charcoal = (22, 24, 30)
deep_slate = (29, 32, 41)
ash_grey = (35, 41, 48)
storm_cloud = (47, 58, 64)
cool_grey = (73, 85, 90)
stone_grey = (105, 125, 128)
blue_grey = (147, 164, 162)
light_concrete = (185, 194, 193)
paper_white = (215, 220, 219)
mist_white = (242, 244, 242)


def dark(color, *args):
    try:
        col2 = list(color)
    except:
        print("Not valid color")
        return

    returnCol = []
    for val in col2:
        if val != 0:
            if args:
                returnCol.append(max(val-args[0], 0))
            else:
                returnCol.append(max(val/2, 0))
        else:
            returnCol.append(val)
    
    return tuple(returnCol)

def light(color, *args):
    try:
        col2 = list(color)
    except:
        print("Not valid color")
        return

    returnCol = []
    for val in col2:
        if args:
            returnCol.append(max(min(val+args[0], 255), 0))
        else:
            returnCol.append(max(min(val*2, 255),0))

    return tuple(returnCol)

def scale_rgb(rgb, factor):
    """Multiply an RGB tuple by a scalar factor and clamp the result to 0–255."""
    return tuple(
        max(0, min(255, int(c * factor)))
        for c in rgb
    )

def rgba(rgb, alpha):
    return tuple([rgb[0], rgb[1], rgb[2], max(min(255, alpha), 0)])
