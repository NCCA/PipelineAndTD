#!/bin/bash

# Configuration
START_FRAME=1
STOP_FRAME=100
STEP=1
TEMPLATE_FILE="teapot.rib"
OUTPUT_DIR="frames"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through frames
for ((frame=$START_FRAME; frame<=$STOP_FRAME; frame+=$STEP)); do
    # Calculate rotation (360 degrees over the full frame range)
    rotation=$(echo "scale=2; $frame * 360 / $STOP_FRAME" | bc)

    # Use sed to replace placeholders and write to output file
    sed -e "s/@FRAME/$frame/g" \
        -e "s/@ROTATION/$rotation/g" \
        "$TEMPLATE_FILE" > "$OUTPUT_DIR/affine_frame_$(printf "%04d" $frame).rib"

    echo "Generated frame $frame with rotation $rotation degrees"
done

echo "Done! Generated $((($STOP_FRAME - $START_FRAME) / $STEP + 1)) frames in $OUTPUT_DIR/"
