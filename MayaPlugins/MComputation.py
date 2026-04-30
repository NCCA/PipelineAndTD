import maya.OpenMaya as OM

interupter = OM.MComputation()
interupter.beginComputation()

quit = False
while not quit:
    for i in range(0, 999):
        if interupter.isInterruptRequested():  # ← check on every iteration
            print("\nInterrupted by escape")
            quit = True
            break  # breaks the for loop
        print(".", end="")

interupter.endComputation() 