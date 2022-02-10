#!/usr/bin/env python
import sys

try:
    from nccapy.timer.Timer import Timer
except:
    print("You need to install the nccapy module and set the pythonpath to point to it")
    sys.exit()

# see here https://tutorial.eyehunts.com/python/python-static-variable-in-a-function-example-code/
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


def getName(text: str) -> str:
    """name is the 4th col in this data so grab it"""
    names = text.split(" ")
    # grab name and strip ""
    name = names[3][1:-1]
    return name


@static_vars(red=0, green=0, blue=0, white=0)
def extractColour(text: str) -> str:
    """colour is the last 3 cols and we are only looking for
    red, green, blue or white"""
    colours = {"100": "Red", "010": "Green", "001": "Blue", "111": "White"}
    text = text.split(" ")
    type = "".join([text[4], text[5], text[6]])
    colour = colours.get(type)
    if colour == "Red":
        extractColour.red += 1
        colourNumber = extractColour.red
    elif colour == "Green":
        extractColour.green += 1
        colourNumber = extractColour.green
    elif colour == "Blue":
        extractColour.blue += 1
        colourNumber = extractColour.blue
    elif colour == "White":
        extractColour.white += 1
        colourNumber = extractColour.white
    return colour + str(colourNumber)


def main(args):
    for f in args[1:]:
        if f.endswith(".ma"):
            with Timer() as tm:
                print("processing ",f)
                with open(f, "r") as mayaFile:
                    scene = mayaFile.readlines()
                for line, text in enumerate(scene):
                    if "pointLight" in text:
                        currentLineIndex = line + 1
                        currentName = getName(text)
                        # Now we need to figure out what colour we have which will come as
                        # and attrib in a later line
                        colourFound = False
                        while colourFound is not True:
                            if ".cl" in scene[currentLineIndex]:
                                colour = extractColour(scene[currentLineIndex])
                                colourFound = True
                            else:
                                currentLineIndex += 1
                        # we now have a name, lets search in the master scene and replace
                        scene[line] = scene[line].replace(currentName, colour)
                        # now we need to change the parent transform name which is
                        parentFound = False
                        currentLineIndex = line
                        while parentFound is not True:
                            if currentName in scene[currentLineIndex]:
                                scene[currentLineIndex] = scene[
                                    currentLineIndex
                                ].replace(currentName, colour)
                                parentFound = True
                            else:
                                currentLineIndex -= 1

                # write out modified file
                with open("Modified" + f, "w") as newFile:
                    newFile.write("".join(scene))


if __name__ == "__main__":
    Timer.add_timer("TotalRun")
    Timer.start_timer("TotalRun")
    main(sys.argv)
    print("Total Run Time {} ms".format(Timer.get_elapsed_ms("TotalRun")))
