import json
from check_availability import check_geoserver_availability

def lambda_handler(event, context):
    path = event.get("rawPath", "/geoserver-availability")
    print(event)
    query_params = event.get("queryStringParameters") or {}
    print(f"Path={path}")

    if path.endswith("/geoserver-availability"):
        page = int(query_params.get("page", 1))
        page_size = int(query_params.get("page_size", 5))
        dataset = "data.json"
        result = check_geoserver_availability(page=page, page_size=page_size, dataset=dataset)

    elif path.endswith("/geoserver-layers"):
        page = int(query_params.get("page", 1))
        page_size = int(query_params.get("page_size", 29))
        dataset = "layer-list.json"
        result = check_geoserver_availability(page=page, page_size=page_size, dataset=dataset)
        result = [item for item in result if item.get("availability") == "OK"]

    else:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Not Found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps(result, indent=4),
    }
