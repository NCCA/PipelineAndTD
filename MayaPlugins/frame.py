import maya.OpenMaya as om
import maya.OpenMayaAnim as oma

anim = oma.MAnimControl()

# Set min and max time
anim.setMinTime(om.MTime(0, om.MTime.uiUnit()))
anim.setMaxTime(om.MTime(100, om.MTime.uiUnit()))

# Access and display start/end info
om.MGlobal.displayInfo(f"start frame = {anim.animationStartTime().value()}")
om.MGlobal.displayInfo(f"end frame = {anim.animationEndTime().value()}")

# Loop through frames in 0.1 steps
end = anim.animationEndTime().value()
i = 0.0
while i < end:
    anim.setCurrentTime(om.MTime(i, om.MTime.uiUnit()))
    om.MGlobal.displayInfo(f"frame = {anim.currentTime().value()}")
    i += 0.1
