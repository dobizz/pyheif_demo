# pyheif_demo
Converts an HEIC image into a PNG image using the `pyheif` package and `FastAPI`

## Installation
```pip install -r requirements.txt```

## Run FastAPI Server
Run either one of the following commands in your terminal
`python main.py` or 
`uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

## Endpoints

### POST

/heif2png ```http://localhost:8000/heif2png```

#### Request Parameters
| Name | Required | Type | Description |
|-------------:|:--------:|:-------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|`save_flag` | optional | bool | Indicates if images are to be saved locally in server<br/>Default is `False` |


#### Request Body
```
files = {
    "file": ("image_file_name", "image_file_bytes")
}
```

#### Sample Responses
```
{
    "status": "ok",
    "format": "heic",
    "heif_file_size": [
        1280,
        720
    ],
    "in_filename": "C001.heic",
    "out_filename": "C001.png",
    "converted_png_data": "base64 encoded image data"
}
```

```
{
    "status": "error",
    "details": "image is not heic format"
}
```

### GET
/docs ```http://localhost:8000/docs```