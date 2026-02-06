#!/bin/bash

# Configuration
START_FRAME=1
STOP_FRAME=100
STEP=1
TEMPLATE_FILE="teapot.rib"

# Loop through frames
for ((frame=$START_FRAME; frame<=$STOP_FRAME; frame+=$STEP)); do
    padded_frame=$(printf "%04d" $frame)
    # Calculate rotation (360 degrees over the full frame range)
    rotation=$(echo "scale=2; $frame * 360 / $STOP_FRAME" | bc)

    echo "Rendering frame $frame with rotation $rotation degrees"

    # Use sed to replace placeholders and pipe directly to prman
    sed -e "s/@FRAME/$padded_frame/g" \
        -e "s/@ROTATION/$rotation/g" \
        "$TEMPLATE_FILE" | prman
done

echo "Done! Rendered $((($STOP_FRAME - $START_FRAME) / $STEP + 1)) frames"
