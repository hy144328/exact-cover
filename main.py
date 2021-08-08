#!/usr/bin/env python3

import json
import os

from algo import Table, AlgorithmX
from cover import io

file_path = os.path.join(
    os.path.dirname(__file__),
    "cover",
    "wiki.json",
)

with open(file_path, 'r') as f:
    wiki_data = json.load(f)
df = io.read_json(wiki_data)
t = Table(df)
print(t)

res, stat = AlgorithmX.solve(t)
print(res)

