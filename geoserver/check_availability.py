import os
from datetime import datetime
import numpy as np
import json
from adress_converter import convert_address_to_lat_lon, convert_lat_lon_to_xyz_coordinates
from tile_downloader import TileDownloader


def is_img_blank(img):
    if img is None:
        return "Geoserver is down"
    if np.all(img == 0) or np.all(img == 255):
        return "Blank image"


def check_geoserver_availability():
    dataset = "data.json"
    tile_downloader = TileDownloader()

    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError("GOOGLE API KEY is missing ")

    test_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(dataset) as f:
        data = json.load(f)

    json_result = []

    for department in data:
        address = department["adresse"]
        coordinates = department["coordonnees"]
        z = 20

        if coordinates == "None":
            lat, lng = convert_address_to_lat_lon(address, key)
            x, y, z = convert_lat_lon_to_xyz_coordinates(lat, lng, z)
        else:
            x, y = map(int, coordinates.split(","))

        departments = department["departement"]

        for layer in departments:
            reason = ""
            processing_time = 0.0
            url = ""

            try:
                image, processing_time, url = tile_downloader.download(y, x, z, "geoserver", layer)
                reason = is_img_blank(image)
                availability = "KO" if reason else "OK"
            except Exception as e:
                print(f"Error downloading or processing image for {address}: {e}")
                availability = "KO"
                reason = str(e)

            json_result.append({
                "department": layer,
                "address": address,
                "position": {"x": x, "y": y, "z": z},
                "availability": availability,
                "reason": reason,
                "tiff_ref": department.get("tiff_ref", None),
                "test_date": test_date,
                "url": url,
                "processing_time": round(processing_time, 1)
            })

        print(f"Processed: {address}, x={x}, y={y}, layers={layer}")

    return json_result


if __name__ == '__main__':
    result = check_geoserver_availability()
    print(json.dumps(result, indent=4, ensure_ascii=False))
