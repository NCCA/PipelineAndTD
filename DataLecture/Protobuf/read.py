#!/usr/bin/env python

import pprint
import sys

import scene_pb2

if __name__ == "__main__" :

    # Main procedure:  Reads the entire address book from a file and prints all
    #   the information inside.
    if len(sys.argv) != 2:
        print ("Usage: {sys.argv[0]} scene file")
        sys.exit(-1)

    scene = scene_pb2.Scene()

    # Read the existing address book.
    f = open(sys.argv[1], "rb")
    scene.ParseFromString(f.read())
    f.close()
    pprint.pprint(scene)
