import os
import json
from datetime import datetime
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

from address_converter import convert_address_to_lat_lon, convert_lat_lon_to_xyz_coordinates
from tile_downloader import TileDownloader


def is_img_blank(img):
    if img is None:
        return "Geoserver is down"
    if np.all(img == 0) or np.all(img == 255):
        return "Blank image"
    return None


def check_geoserver_availability(page=1, page_size=5, max_workers=10):
    dataset = "data.json"
    tile_downloader = TileDownloader()

    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError("GOOGLE API KEY is missing")

    test_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(dataset) as f:
        data = json.load(f)

    # Pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_data = data[start_idx:end_idx]

    results = []

    def process_layer(address, coordinates, z, layer, tiff_ref):
        try:
            if coordinates == "None":
                lat, lng = convert_address_to_lat_lon(address, key)
                x, y, z = convert_lat_lon_to_xyz_coordinates(lat, lng, z)
            else:
                x, y = map(int, coordinates.split(","))

            image, processing_time, url = tile_downloader.download(y, x, z, "geoserver", layer)
            reason = is_img_blank(image)
            print(f"{url}")
            availability = "KO" if reason else "OK"
        except Exception as e:
            availability = "KO"
            reason = str(e)
            url = ""
            processing_time = 0.0
        return {
            "department": layer,
            "address": address,
            "position": {"x": x, "y": y, "z": z},
            "availability": availability,
            "reason": reason,
            "tiff_ref": tiff_ref,
            "test_date": test_date,
            "url": url,
            "processing_time": round(processing_time, 1),
        }

    futures = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for department in paginated_data:
            address = department["adresse"]
            coordinates = department["coordonnees"]
            z = 20
            for layer in department["departement"]:
                futures.append(
                    executor.submit(
                        process_layer, address, coordinates, z, layer, department.get("tiff_ref")
                    )
                )

        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"Processed: {result['address']}, x={result['position']['x']}, "
                  f"y={result['position']['y']}, layer={result['department']}")

    return results
