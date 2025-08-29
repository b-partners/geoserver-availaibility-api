import json

from geoserver.check_availability import check_geoserver_availability


def lambda_handler(event, context):
    result = check_geoserver_availability()
    return {
        "statusCode": 200,
        "body": json.dumps(result, indent=4),
    }
