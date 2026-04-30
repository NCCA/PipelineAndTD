import time

import maya.OpenMaya as OM

# as these can take time to process we have an interupter to allow for the process to be
# stopped
interupter = OM.MComputation()
# set the start of the heavy computation
# True here means the progress bar will be displayed
interupter.beginComputation(True)
interupter.setProgressRange(0, 1000)

for i in range(0, 1000):
    interupter.setProgress(i)
    if interupter.isInterruptRequested():
        print("intrupted by escape")
        break
    print(".", end="")
    time.sleep(0.01)
interupter.endComputation()
