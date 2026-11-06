import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('serverless-database')

def handler(event, context):
    # ignore when the browser asks for an favicon icon
    if event.get('rawPath') == '/favicon.ico':
        return {
            'statusCode': 200,
            'body': json.dumps('Ignored favicon')
        }

    # then count the visitor normally
    response = table.update_item(
        Key={'id': 'visitors'},
        UpdateExpression='ADD visit_count :inc',
        ExpressionAttributeValues={':inc': 1},
        ReturnValues='UPDATED_NEW'
    )
    
    count = int(response['Attributes']['visit_count'])
    
    return {
        'statusCode': 200,
        'body': json.dumps({'visit_count': count})
    }