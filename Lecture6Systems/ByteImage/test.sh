#!/bin/bash

 YourApp | ffmpeg -f rawvideo -pixel_format rgba -video_size 400x400  -i - -preset slow -c:v libx264 -y ./test.mp4