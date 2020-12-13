import boto3
from boto3.dynamodb.conditions import Key

from environment import DYNAMODB_TABLE_NAME, POOL_TEMPERATURE_SENSOR_ID


def query_pool_temperature(current_datetime, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    milliseconds = int(round(current_datetime.time() * 1000))
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.query(
        KeyConditionExpression=(Key("sensorId").eq(POOL_TEMPERATURE_SENSOR_ID)
                                & Key('timestamp').gt(milliseconds-(3600*1000))),
        Limit=1
    )
    result = None
    if len(response['Items']) == 1:
        result = response['Items'][0]['sensor_value']
    return result

