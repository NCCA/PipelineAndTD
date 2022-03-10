#!/usr/bin/env python
import platform
import random
import subprocess
import sys

sys.path.insert(0, "../ByteImage")
import ByteImage


def main():
    if platform.system() == "Darwin":
        ffmpeg = "/Applications/ffmpeg"
    else:
        ffmpeg = "ffmpeg"  # it should be in the path
    # fmt:off
    command = [
        ffmpeg,"-f","rawvideo","-pixel_format",
        "rgba", "-video_size", "400x400", "-framerate",
        "24", "-i", "-", "-vcodec", "mpeg4", "-y", "movie.mp4",
    ]
    # fmt:on

    # going to create our pipe / process
    pipe = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL,
        bufsize=10**8,
    )

    rx = random.randint
    img = ByteImage.ByteImage(400, 400, 255, 0, 0, 255)

    for i in range(0, 200):
        img.clear(255, 255, 255)
        cx = rx(1, img.width)
        cy = rx(1, img.height)
        for x in range(0, 1000):
            img.line(
                cx,
                cy,
                rx(1, img.width - 1),
                rx(1, img.height - 1),
                rx(0, 255),
                rx(0, 255),
                rx(0, 255),
            )
        pipe.stdin.write(img.pixels)


if __name__ == "__main__":
    main()
