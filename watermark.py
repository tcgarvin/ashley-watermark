from os import getenv, mkdir
from pathlib import Path
import sys
from time import time
from traceback import print_exc
from typing import Iterable

from PIL import Image

RELATIVE_OUTPUT_DIR = "watermarked"
RIGHT_PADDING_COEFFICIENT = 1.2


def watermark_image(target_image : Image.Image, watermark : Image.Image) -> None:
    watermark_width_limit_ratio = target_image.width / 2 / watermark.width
    watermark_height_limit_ratio = target_image.height / 3 / watermark.width
    watermark_resize_ratio = min(
        watermark_height_limit_ratio, 
        watermark_width_limit_ratio
    )

    resized_watermark = watermark.resize((
        int(watermark.width * watermark_resize_ratio), 
        int(watermark.height * watermark_resize_ratio)
    ))

    target_image.paste(
        resized_watermark, 
        (
            target_image.width - int(resized_watermark.width * RIGHT_PADDING_COEFFICIENT),
            target_image.height - resized_watermark.height
        ),
        resized_watermark
    )


def watermark_file(target_file : Path, watermark : Image.Image) -> None:
    target_image = Image.open(target_file)
    watermark_image(target_image, watermark)
    target_image.save(generate_output_path(target_file))


def fetch_watermark() -> Image.Image:
    watermark_path = getenv("WATERMARK_PATH", None)
    if watermark_path is None:
        watermark_path = f'{getenv("HOME")}/.watermark/watermark.png'

    return Image.open(watermark_path)


def locate_target_files(search_path : Path) -> Iterable[Path]:
    target_files = []
    for file_path in search_path.iterdir():
        if file_path.suffix not in (".png", ".jpg", ".jpeg"):
            continue

        output_path = generate_output_path(file_path)

        if output_path.exists():
            print(f"Already created watermarked {file_path.name}, skipping.")
            continue

        target_files.append(file_path)

    return target_files


def generate_output_path(input_path : Path) -> Path:
    return input_path.parent / RELATIVE_OUTPUT_DIR / input_path.name


def watermark_dir(target_dir : Path, watermark : Image.Image) -> None:
    start_time = time()
    print(f"Watermarking images in {target_dir}...")

    target_files = locate_target_files(target_dir)

    (target_dir / RELATIVE_OUTPUT_DIR).mkdir(exist_ok=True)

    errors = 0
    for target_file in target_files:
        try:
            print(f"Watermarking {target_file.name}...", end="")
            watermark_file(target_file, watermark)
            print("done")

        except IOError as e:
            errors += 1
            print()
            print(f"An error occured when processing {target_file.name}. Skipping")
            print_exc()
            print()

    end_time = time()
    duration = int(end_time - start_time)
    good_count = len(target_files) - errors
    if errors == 0:
        print(f"Watermarked {good_count} images in {duration} seconds.")
    else:
        print(f"Watermarked {good_count} images in {duration} seconds, with {errors} errors")


if __name__ == "__main__":
    target_dir = Path(sys.argv[1])
    watermark = fetch_watermark()
    watermark_dir(target_dir, watermark)
