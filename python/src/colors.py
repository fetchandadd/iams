import json
import math

# config
frequency_round_digits = 4
thumbnail_size = 16, 16
max_colors = 256


def compute_top_colors_of_image(image, number_of_colors=5):
    html_colors = load_html_colors()
    html_color_values = list(html_colors.values())
    colors = get_colors_from_image(image)
    colors = classify_color_list(colors, html_color_values)
    colors_counted = count_color_classes(colors)
    colors_counted_normalized_frequency = normalize_frequency(colors_counted)
    colors_hex = list(colors_counted_normalized_frequency.keys())
    colors = build_result_color_list(colors_hex,
                                     colors_counted_normalized_frequency,
                                     html_colors)
    colors = sort_colors_by_frequency(colors)
    number_of_colors = restrict_number_of_colors(colors, number_of_colors)
    return colors[:number_of_colors]


def restrict_number_of_colors(colors, number_of_colors):
    return max(1, min(len(colors), number_of_colors))


def normalize_frequency(colors_counted):
    count_of_pixels = count_pixels(colors_counted)
    for key, value in colors_counted.items():
        colors_counted[key] = round(value / count_of_pixels,
                                    frequency_round_digits)
    return colors_counted


def count_pixels(color):
    i = 0
    for key, value in color.items():
        i += value
    return i


def build_result_color_list(color_hex, colors_counted, html_colors):
    return list(
        map(lambda x: build_result_item(x, colors_counted, html_colors),
            color_hex))


def build_result_item(hex_color, frequencies, html_colors):
    return {'color': html_colors[hex_color],
            'frequency': frequencies[hex_color]}


def get_colors_from_image(image):
    test_image_pillow = image.copy()
    test_image_pillow.thumbnail(size=thumbnail_size)
    test_image_pillow = test_image_pillow.convert("RGB")
    image_colors_rgb = test_image_pillow.getcolors(maxcolors=max_colors)
    return list(map(convert_frequency_rgb_tuple_to_dict, image_colors_rgb))


def load_html_colors():
    with open('./colors.json') as color_file:
        return json.load(color_file)


def build_color(color):
    """(0,0,0) -> {'r': 0, 'g': 0, 'b':0}"""
    return {'r': color[0], 'g': color[1], 'b': color[2]}


def convert_frequency_rgb_tuple_to_dict(frequency_rgb_tuple):
    frequency = frequency_rgb_tuple[0]
    rgb = frequency_rgb_tuple[1]
    return {'frequency': frequency, 'rgb': build_color(rgb)}


def count_color_classes(colors):
    arr = {}
    for color in colors:
        try:
            arr[color['color_class']] += color['frequency']
        except KeyError:
            arr[color['color_class']] = color['frequency']
    return arr


def sort_colors_by_frequency(colors):
    return sorted(colors, key=lambda color: color['frequency'],
                  reverse=True)


def euclid_distance(x, y):
    """{'r':2, 'g':1, 'b':3}, {'r':0, 'g':0, 'b':0} -> 3.7416573868"""
    return math.sqrt((x['r'] - y['r']) ** 2 +
                     (x['g'] - y['g']) ** 2 +
                     (x['b'] - y['b']) ** 2)


def classify_color_list(colors, html_color_values):
    return list(map(lambda x: classify_color(x, html_color_values), colors))


def classify_color(frequency_rgb_dict, html_color_values):
    color_class = get_color_class(frequency_rgb_dict['rgb'],
                                  html_color_values)
    return {'frequency': frequency_rgb_dict['frequency'],
            'color_class': color_class}


def get_color_class(color, html_color_values):
    """{'r': 0, 'g': 0, 'b':0} -> 000000"""
    return min(distance_to_color_class(color, html_color_values),
               key=lambda x: x['distance'])[
        'hex']


def distance_to_color_class(target_color, html_color_values):
    return list(map(lambda x: {'hex': x['hex'],
                               'distance': euclid_distance(x,
                                                           target_color)},
                    html_color_values))
