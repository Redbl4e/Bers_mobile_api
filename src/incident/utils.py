import shutil
from pathlib import Path
from pprint import pprint
from uuid import uuid4

from fastapi import UploadFile
from geopy import Yandex
from geopy.location import Location

from src.config import MEDIA_PATH, YANDEX_GEOCODER_API_KEY


def get_address_from_coords(longitude: float, latitude: float) -> str:
    geolocator = Yandex(api_key=YANDEX_GEOCODER_API_KEY,
                        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                        timeout=5)
    address: Location = geolocator.reverse(f"{latitude}, {longitude}", lang="ru", timeout=5)
    formatted_address = _format_address(address)
    print(formatted_address)
    return formatted_address


def _format_address(address) -> str:
    components = address.raw.get("metaDataProperty").get("GeocoderMetaData").get("Address").get("Components")
    for component in components[2:]:
        kind = component.get("kind")
        match kind:
            case "locality":
                city = component.get("name")
            case "street":
                street = component.get("name")
            case "house":
                house = component.get("name")
    address_str = f"г. {city}, {street}, {house}"
    return address_str


def save_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def get_unique_filename(filename: str) -> Path:
    filename, *extension = filename.split(".")
    extension = ".".join(extension)
    filename = f"{filename}_{uuid4()}.{extension}"
    file_path = MEDIA_PATH / f"posts/{filename}"
    return file_path


if __name__ == "__main__":
    get_address_from_coords(30.331948, 59.888212)
