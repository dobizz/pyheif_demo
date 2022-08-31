import base64
import io
import os
from pathlib import Path

import pyheif
import uvicorn
import whatimage
from fastapi import FastAPI, UploadFile
from PIL import Image

from config import ACCESS_LOG, HOST, IMAGES_DIR, PORT, RELOAD

app = FastAPI()


@app.post("/heif2png")
async def convert_heif(file: UploadFile, save_flag:bool=False):
    # Input files for validation available at
    # https://github.com/nokiatech/heif_conformance/tree/master/conformance_files

    # read bytes from uploaded file
    image_bytes = await file.read()

    # get base filename from uploaded file
    filename = Path(file.filename).stem

    fmt = whatimage.identify_image(image_bytes)
    # check if image uploaded is correct format
    if fmt != "heic":
        return {"status": "error", "details": "image is not heic format"}

    # process heif image
    heif_file = pyheif.read(image_bytes)

    # convert heif bytes to PIL image
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )

    # save locally as PNG
    if save_flag:
        # create directory if it does not exist
        if not os.path.exists(IMAGES_DIR):
            os.mkdir(IMAGES_DIR)
        # save original image to directory
        with open(Path(IMAGES_DIR, file.filename), "wb") as f:
            f.write(image_bytes)
        # save converted image to directory
        image.save(Path(IMAGES_DIR, filename).with_suffix(".png"), format="png")

    # save png image to buffer
    with io.BytesIO() as output:
        image.save(output, format="png")
        png_image = output.getvalue()

    # serialize png image
    png_image = base64.b64encode(png_image)

    # return HTTP response to caller
    return {"status": "ok", "format": fmt, "heif_file_size": heif_file.size, "in_filename": file.filename, "out_filename": f"{filename}.png","converted_png_data": png_image}


if __name__ == '__main__':
    # visit http://localhost:8000/docs for help
    uvicorn.run("main:app", host=HOST, port=PORT, reload=RELOAD, access_log=ACCESS_LOG)