import json
import boto3

# link to dynamodb
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('serverless-database')

def handler(event, context):
    # instruct the database to find the 'visitors' tally and add +1
    response = table.update_item(
        Key={'id': 'visitors'},
        UpdateExpression='ADD views :inc',
        ExpressionAttributeValues={':inc': 1},
        ReturnValues='UPDATED_NEW'
    )
    
    # extract the most recent total number from the database response
    views = int(response['Attributes']['views'])
    
    # send the total number back to the website
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*' # gives website access to read the data
        },
        'body': json.dumps({'views': views})
    }