from typing import Any
from PIL import Image
from PIL.ExifTags import TAGS

def get_image_meta(file: str) -> dict[str, Any]:
    image = Image.open(file)
    exifdata = image.getexif()
    image_meta: dict[str, Any] = {}
    for key, value in exifdata.items():
        tag = TAGS.get(key, key)
        if isinstance(tag, str):
            image_meta[tag] = value
    return image_meta
