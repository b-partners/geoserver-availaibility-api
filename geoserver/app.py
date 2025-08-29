import json

from check_availability import check_geoserver_availability

def lambda_handler(event, context):
    query_params = event.get("queryStringParameters") or {}
    page = int(query_params.get("page", 1))
    page_size = int(query_params.get("page_size", 5))

    result = check_geoserver_availability(page=page, page_size=page_size)

    return {
        "statusCode": 200,
        "body": json.dumps(result, indent=4),
    }