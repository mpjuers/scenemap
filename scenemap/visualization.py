#!/usr/bin/env python3
# Cleans the json input and prepares a DataFrame.

import json
import sys

from bokeh import plotting as plt
from bokeh.io import show
import networkx as nx
import pandas as pd


def pre_format(path):
    with open(path) as file:
        data_dict = json.load(file)
        df = pd.json_normalize(data_dict, max_level=2)
        df_melted = df.melt(id_vars="artist")
        return df_melted.explode("value")


def _format(df, connections):
    df_filtered = df[df["variable"] == connections][["artist", "value"]]
    df_filtered.set_index("artist")
    return df_filtered


def generate_figure(df, connections="artist", *args):
    TOOLTIPS = [(connections, "@index")]
    p0 = plt.figure(
        plot_width=300, plot_height=300,
        x_range=(-1.1, 1.1), y_range=(-1.1, 1.1),
        tooltips=TOOLTIPS
    )
    # Will error if there are NaNs.
    df_formatted = _format(df, connections, *args).dropna()
    G = nx.from_pandas_edgelist(
        df_formatted, "artist", "value"
    )
    graph = plt.from_networkx(
        G, nx.spring_layout
    )
    p0.renderers.append(graph)
    show(p0)


def main():
    df = pre_format(sys.argv[1])
    generate_figure(df, "genres")
    

if __name__ == "__main__":
    main()
