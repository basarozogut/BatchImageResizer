def parse_image_sizes(text):
    # parse the text: 640x480,320x240,120x120 etc. into a list of tuples.
    sizes_text = text.split(",")
    parsed = []
    for txt in sizes_text:
        width_height = txt.split("x")
        w = int(width_height[0])
        h = int(width_height[1])
        t = (w, h)
        parsed.append(t)

    return parsed