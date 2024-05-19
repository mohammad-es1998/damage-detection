from PIL import Image, ImageDraw

damage_areas = {
    'Bonnet': [(356, 343), (366, 174), (412, 159), (599, 159), (647, 174), (658, 342), (612, 318), (576, 309),
               (517, 308), (444, 309), (431, 312), (413, 314), (356, 342)],  # Front view bonnet
    'Front Door': [(356, 343), (366, 174), (412, 159), (599, 159), (647, 174), (658, 342), (612, 318), (576, 309),
                   (517, 308), (444, 309), (431, 312), (413, 314), (356, 342)],
    'Roof': [
        [(625, 461), (618, 477), (620, 821), (509, 829), (396, 822), (397, 475), (390, 460), (441, 452), (507, 450),
         (566, 451), (623, 460)],  # Top view roof
    ],
    'Trunk': [
        (392, 974), (446, 968), (502, 964), (562, 967), (625, 974), (629, 1023),
        (662, 1022), (662, 1029), (351, 1029), (352, 1019), (391, 1022), (390, 972)],
    'Back Door': [
        (392, 974), (446, 968), (502, 964), (562, 967), (625, 974), (629, 1023),
        (662, 1022), (662, 1029), (351, 1029), (352, 1019), (391, 1022), (390, 972)],
}


def generate_polygons(damaged_parts):
    # Load the image
    image_path = 'car-parts2.png'  # Replace with the path to your image file
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for damaged_part in damaged_parts:
        areas = damage_areas[damaged_part]
        if isinstance(areas[0], tuple):
            # If single polygon
            draw.polygon(areas, outline="blue", fill="blue")
        else:
            # Multiple polygons
            for area in areas:
                draw.polygon(area, outline="blue", fill="blue")

    # Save or display the image
    output_path = 'damage_highlighted.png'
    image.resize((2000, 2000)).save(output_path)
    return output_path
