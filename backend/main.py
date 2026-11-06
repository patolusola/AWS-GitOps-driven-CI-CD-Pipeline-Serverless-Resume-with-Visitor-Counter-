import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('serverless-database')

def handler(event, context):
    # instruct the database to find the visitors tally and add it +1
    response = table.update_item(
        Key={'id': 'visitors'},
        UpdateExpression='ADD visit_count :inc',
        ExpressionAttributeValues={':inc': 1},
        ReturnValues='UPDATED_NEW'
    )
    
    # extract the most recent total number from the database response
    count = int(response['Attributes']['visit_count'])
    
    # send the total number back to the website
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*' 
        },
        'body': json.dumps({'visit_count': count})
    }