#!/usr/bin/env -S uv run --active --script

import json
from pprint import pprint

with open("scene.json") as f:
    scene = json.load(f)

pprint(scene)
