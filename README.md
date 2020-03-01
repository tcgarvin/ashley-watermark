# Watermarking tool with MacOS integration

Quick watermarking scripting, using [pillow](https://pillow.readthedocs.io/en/stable/).

## Installation

This is a single-install type of project, so install is a little tricky, and installation options are nil.  Here's one way you can do it, but you can probably come up with a better one.  Lots of the file locations are hard-coded, so you'll have to change the code to make things better.

1. Setup a virtual environment, take note of it's location.
1. Install pillow, as noted in `requirements.txt`.
1. Drop `watermark.sh` in your home directory.
1. Drop your watermark image into `~/.watermark/watermark.png`
1. Edit `watermark.sh` to use your virtual environment and to point to `watermark.py` in your repo.
1. Copy the Bash script in `quickaction.sh` into a quick action script in MacOS Automator

## Usage

You should be able to right click on a folder in finder, and run your quickaction.  Every `.png` and `.jpg` in the target folder will be watermarked in the lower-right corner.  The watermarked version of the image will be placed in the `watermarked` directory inside the target directory.