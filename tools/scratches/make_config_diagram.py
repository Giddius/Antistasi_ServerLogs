from graphviz import Digraph, Graph, FORMATS, FORMATTERS, RENDERERS
import os
import shutil
import subprocess
from antipetros_discordbot.utility.gidtools_functions import pathmaker, loadjson, writejson
from configparser import ConfigParser
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from pprint import pprint
from icecream import ic
import random


APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

COLOR_LIST = loadjson(pathmaker(THIS_FILE_DIR, '../resources/data/graphviz_colors.json'))

for i in range(70, 100, 5):
    COLOR_LIST.append(f"gray{i}")
for _ in range(100):
    random.shuffle(COLOR_LIST)
colors_i_like = list(set(["oldlace",
                          "burlywood1",
                          "palegoldenrod",
                          "tan",
                          "lightblue1",
                          "azure1",
                          "lightpink3",
                          "thistle3",
                          "lightgoldenrodyellow",
                          "lightcyan3",
                          "lightblue3",
                          "lavenderblush3",
                          "bisque",
                          "lightyellow3",
                          "palegreen",
                          "lightslategrey",
                          "gray75",
                          "cornflowerblue",
                          "navajowhite",
                          "darkslategray2",
                          "blanchedalmond",
                          "ivory3",
                          "blue3",
                          "wheat2",
                          "gray80",
                          "orchid",
                          "lavenderblush2",
                          "plum3",
                          "honeydew",
                          "cadetblue3",
                          "sandybrown",
                          "wheat1",
                          "seagreen3",
                          "gold",
                          "pink1",
                          "aquamarine",
                          "lightsteelblue1",
                          "darkseagreen1",
                          "gray85",
                          "mistyrose",
                          "linen",
                          "snow3",
                          "gainsboro",
                          "gray80",
                          "khaki2",
                          "lightgray",
                          "lightgrey",
                          "mintcream",
                          "papayawhip",
                          "seashell",
                          "seashell3",
                          "peachpuff1",
                          "mistyrose2",
                          "honeydew3",
                          "grey93",
                          "cornsilk1",
                          "chartreuse3"]))

existing_colors = []


def random_color_funct():
    global existing_colors
    random.shuffle(COLOR_LIST)
    color = random.choice(COLOR_LIST)
    if color not in existing_colors:
        existing_colors.append(color)
        return color
    return random_color_funct()


random_color = random_color_funct


def make_config_dict(in_config):
    config_dict = {}
    for section in in_config.sections():
        config_dict[section] = []
        for option in in_config.options(section):
            if not option.startswith('#'):
                config_dict[section].append(option)
    return config_dict


gradient = 'papayawhip:lightgoldenrod3'
font_size_base = 20.0


def make_config_graph(in_config):
    graph_name = os.path.basename(in_config.config_file).split('.')[0].upper()
    graph = Digraph(name=graph_name, edge_attr={})
    graph.attr(rankdir='LR', splines='false', nodesep='0.3', compound="true", ranksep="2.0", packmode='node', pack='true')
    graph.node(graph_name, shape="rarrow", style="filled", fillcolor="lightseagreen", fontsize=str(font_size_base * 1.5), margin="0.25")
    graph.node('invisi', "", style="invis", shape="point")
    graph.edge(graph_name, "invisi", arrowhead="none")
    for key, value in make_config_dict(in_config).items():
        graph.node(key, shape="box3d", style="filled", fillcolor="olivedrab3", fontsize=str(font_size_base))
        graph.edge("invisi", key, headport='w', arrowhead="none")
        # graph.edge(graph_name, key, rank="same", headport='w')
        with graph.subgraph(name='cluster_' + key, graph_attr={'style': 'filled', 'fillcolor': gradient, 'rank': "same", "ranksep": "0.25"}) as subg:
            for option in value:
                color = random_color()
                print(option + '  --  ' + color)
                subg.node(key + option, option, shape="component", style="filled", fillcolor=color, fontsize=str(font_size_base))
                subg.edge(key, key + option, headport="w", tailport='e', arrowhead="none")
    print(len(existing_colors))
    print(len(colors_i_like))

    graph.render('test_graph', format='png', cleanup=True)


if __name__ == '__main__':
    make_config_graph(BASE_CONFIG)
