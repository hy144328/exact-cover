#!/usr/bin/env python3

import json
import os
import pandas as pd

def read_json(data):
    rows = list(data.keys())
    no_rows = len(rows)

    cols = set()
    cols = list(cols.union(*data.values()))
    no_cols = len(cols)

    df = pd.DataFrame(
        0,
        index=rows,
        columns=cols,
        dtype=int,
    )
    for row_it in data:
        df.loc[row_it, data[row_it]] = 1

    return df

if __name__ == "__main__":
    file_path = os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        "cover",
        "wiki.json",
    )

    with open(file_path, 'r') as f:
        wiki_data = json.load(f)
    df = read_json(wiki_data)

    print(df)
