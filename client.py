
import base64
import glob
import os
from pathlib import Path

import requests
import whatimage

from config import IMAGES_DIR


def main() -> None:
    url = "http://localhost:8000/heif2png"
    # loop through each heic image in images directory
    for file in glob.glob(os.path.join(IMAGES_DIR, "*.heic")):
        print(file)

        # open file and read bytes
        with open(file, "rb") as in_file_handler:
            image_bytes = in_file_handler.read()

        # filter out images saved as heic but not actually heic
        # when checking the file signature
        if whatimage.identify_image(image_bytes) != "heic":
            continue

        # create payload, {"file": (file_name, file_bytes)}
        files = {
            "file": (os.path.basename(file), image_bytes),
        }

        # make post request to /heif2png endpoint
        result = requests.post(url, files=files)

        result.raise_for_status()

        result = result.json()

        # decode image
        base64_image = result["converted_png_data"]
        base64_bytes = base64.b64decode(base64_image)

        # save converted image
        with open(Path(IMAGES_DIR, result["out_filename"]), "wb") as out_file_handler:
            out_file_handler.write(base64_bytes)


if __name__ == '__main__':
    main()

