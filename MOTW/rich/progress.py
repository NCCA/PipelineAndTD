#!/usr/bin/env python
from rich.progress import track

def do_work(s) :
    for i in range(0,10000000) :
        pass


for step in track(range(100)):
    do_work(step)