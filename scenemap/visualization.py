#!/usr/bin/env python3
# Cleans the json input and prepares a DataFrame.

import json
import sys

from bokeh import plotting as plt
from bokeh.io import show
import networkx as nx
import pandas as pd
import wikipedia


class Dataset:
    def __init__(self, path="../DataFiles/albumData.json"):
        self.path = path
        self.data = self._format()

    def pre_format(self):
        with open(self.path) as file:
            data_dict = json.load(file)
            df = pd.json_normalize(
                data_dict["items"],
                record_path=["album", "tracks", "items", "artists"],
                errors="ignore",
            )
            df_melted = df.melt(value_vars="name")
            out = df_melted
            print(out)
            return out

    def _format(self, connections="artists"):
        data = self.pre_format()
        df_filtered = data[data["variable"] == connections][
            ["variable", "value"]
        ]
        df_filtered.set_index("value")
        return df_filtered


# class Wikidata:

#     def __init__(self, path="../DataFiles/albumData"):
#         for artist in pre_format(path):


def generate_figure(df, connections="artist", *args):
    TOOLTIPS = [(connections, "@index")]
    p0 = plt.figure(
        plot_width=300,
        plot_height=300,
        x_range=(-1.1, 1.1),
        y_range=(-1.1, 1.1),
        tooltips=TOOLTIPS,
    )
    # Will error if there are NaNs.
    df_formatted = Dataset()
    G = nx.from_pandas_edgelist(df_formatted, "artist", "value")
    graph = plt.from_networkx(G, nx.spring_layout)
    p0.renderers.append(graph)
    show(p0)


def main():
    df = Dataset()
    print(df.data.head())
    return 0


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
