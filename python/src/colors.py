from colors_database import html_colors_dict
from colors_database import html_colors_list
from functools import reduce
from typing import List, Dict
import cherrypy
import math

# config
frequency_round_digits = 4
thumbnail_size = 16, 16
max_colors = 256


def compute_top_colors_of_image(image, number_of_colors: int = 5):
    """
    :param image: Pillow image object
    :param number_of_colors: 5
    :return: [{'color':{'name':'Blue', 'hex':'0000FF', 'r':0, 'g':0, 'b':255}, 'frequency':0.4}, ...]
    """
    colors = get_colors_from_image(image)
    colors = classify_color_list(colors, html_colors_list)
    colors = count_color_classes(colors)
    colors = normalize_frequency(colors)
    colors = build_result_color_list(colors, html_colors_dict)
    colors = sort_colors_by_frequency(colors)
    number_of_colors = restrict_number_of_colors(colors, number_of_colors)
    return colors[:number_of_colors]


def restrict_number_of_colors(colors: List, number_of_colors: int) -> int:
    """
    :param colors: [{'color':{'name':'Black', 'hex':'000000', 'r':0, 'g':0, 'b':0}, 'frequency':0.3}, ...]
    :param number_of_colors: 5
    :return:5
    """
    if number_of_colors < 1:
        raise cherrypy.HTTPError(400, 'Parameter n must be greater or equal 1')
    return min(len(colors), number_of_colors)


def normalize_frequency(colors: Dict) -> Dict:
    """
    :param colors: {'000000':4, 'FFFFFF':2, ... }
    :return: {'000000':0.3, 'FFFFFF':0.2, ... }
    """
    base = summarize_frequencies(colors)
    for hex_color, frequency in colors.items():
        colors[hex_color] = normalize_frequency_and_round(frequency, base)
    return colors


def normalize_frequency_and_round(frequency: int, base: int) -> float:
    """
    :param frequency: 3
    :param base: 14
    :return:0,2142
    """
    return round(frequency / base, frequency_round_digits)


def summarize_frequencies(color: Dict) -> int:
    """
    :param color: {'000000':5, 'FFFFFF':8, ... }
    :return: >= 13
    """
    return reduce(lambda x, y: x + y, color.values())


def build_result_color_list(colors: Dict, html_colors: Dict) -> List:
    """
    :param colors: ['000000', 'FFFFFF', ... ]
    :param html_colors: {'000000':{'name':'Black', 'hex':'000000', 'r':0, 'g':0, 'b':0}, ...}
    :return: [{'color':{'name':'Black', 'hex':'000000', 'r':0, 'g':0, 'b':0}, 'frequency':0.3}, ...]
    """
    colors_hex = list(colors.keys())
    color_iter = map(lambda x: build_item(x, colors, html_colors), colors_hex)
    return list(color_iter)


def build_item(hex_color: str, frequencies: Dict, html_colors: Dict) -> Dict:
    """
    :param hex_color: '000000'
    :param frequencies: {'000000':0.3, 'FFFFFF':0.2, ... }
    :param html_colors:{'000000':{'name':'Black', 'hex':'000000', 'r':0, 'g':0, 'b':0}, ...}
    :return: {'color':{'name':'Black', 'hex':'000000', 'r':0, 'g':0, 'b':0}, 'frequency':5}
    """
    return {'color': html_colors[hex_color],
            'frequency': frequencies[hex_color]}


def get_colors_from_image(image) -> List:
    """
    :param image: Pillow image object
    :return: [[5,[0,0,0], [8,(255,255,255), ...]
    """
    image.thumbnail(size=thumbnail_size)
    image = image.convert('RGB')
    colors = image.getcolors(maxcolors=max_colors)
    return list(map(convert_frequency_rgb_tuple_to_dict, colors))


def build_color(color: List) -> Dict:
    """
    :param color: [0,0,0]
    :return: {'r':0, 'g':0, 'b':0}
    """
    return {'r': color[0], 'g': color[1], 'b': color[2]}


def convert_frequency_rgb_tuple_to_dict(frequency_rgb_tuple: List) -> Dict:
    """
    :param frequency_rgb_tuple: [5,[0,0,0]]
    :return: {'frequency':5, 'rgb':{'r':0, 'g':0, 'b':0}}
    """
    return {'frequency': frequency_rgb_tuple[0],
            'rgb': build_color(frequency_rgb_tuple[1])}


def count_color_classes(colors: List[Dict]) -> Dict:
    """
    :param colors: [{'frequency':5, 'color_class':'000000'}, ...]
    :return: {'000000':5, 'FFFFFF': 8, ... }
    """
    color_dict = {}
    for color in colors:
        try:
            color_dict[color['color_class']] += color['frequency']
        except KeyError:
            color_dict[color['color_class']] = color['frequency']
    return color_dict


def sort_colors_by_frequency(colors: List) -> List:
    """
    :param colors: [{'color':{'name':'Black', 'hex':'000000', 'r':0, 'g':0, 'b':0}, 'frequency':0.3}, ...]
    :return: [{'color':{'name':'Blue', 'hex':'0000FF', 'r':0, 'g':0, 'b':255}, 'frequency':0.4}, ...]
    """
    return sorted(colors,
                  key=lambda color: color['frequency'],
                  reverse=True)


def euclid_distance(x: Dict, y: Dict) -> float:
    """
    :param x: {'r':2, 'g':1, 'b':3}
    :param y: {'r':0, 'g':0, 'b':0}
    :return: 3.7416573868
    """
    return math.sqrt((x['r'] - y['r']) ** 2 +
                     (x['g'] - y['g']) ** 2 +
                     (x['b'] - y['b']) ** 2)


def classify_color_list(colors: List, html_color_values: List) -> List:
    """
    :param colors: [{'rgb':{'r':0, 'g':0, 'b':0}, 'frequency':5}, ...]
    :param html_color_values: [{'name':'Black', 'hex':'000000', 'r':0, 'g':0, 'b':0}, ...]
    :return: [{'frequency':5, 'color_class':'000000'}, ...]
    """
    return list(map(lambda x: classify_color(x, html_color_values), colors))


def classify_color(frequency_rgb_dict: Dict, html_color_values: List) -> Dict:
    """
    :param frequency_rgb_dict: {'rgb':{'r':0, 'g':0, 'b':0}, 'frequency':5}
    :param html_color_values: [{'name':'Black', 'hex':'000000', 'r':0, 'g':0, 'b':0}, ...]
    :return: {'frequency':5, 'color_class':'000000'}
    """
    color_class = get_color_class(frequency_rgb_dict['rgb'],
                                  html_color_values)
    return {'frequency': frequency_rgb_dict['frequency'],
            'color_class': color_class}


def get_color_class(color: Dict, html_color: List) -> str:
    """
    :param color: {'r':0, 'g':0, 'b':0}
    :param html_color: [{'name':'Black', 'hex':'000000', 'r':0, 'g':0, 'b':0},...]
    :return: '000000'
    """
    color_distance_list = distance_to_color_class(color, html_color)
    closest_color = min(color_distance_list, key=lambda x: x['distance'])
    return closest_color['hex']


def distance_to_color_class(target_color: Dict, html_colors: List) -> List:
    """
    :param target_color: {'r':0, 'g':0, 'b':0}
    :param html_colors: [{'name':'Black', 'hex':'000000', 'r':0, 'g':0, 'b':0},...]
    :return: [{'hex':'000000', distance:0},...]
    """
    iterator = map(lambda x: build_hex_distance(x, target_color), html_colors)
    return list(iterator)


def build_hex_distance(html_color: Dict, target_color: Dict) -> Dict:
    """
    :param html_color: {'r':0, 'g':0, 'b':0}
    :param target_color: {'name':'Black', 'hex':'000000', 'r':0, 'g':0, 'b':0}
    :return: {'hex':'000000', distance:0}
    """
    distance = euclid_distance(html_color, target_color)
    return {'hex': html_color['hex'], 'distance': distance}
