import json
import base64
import boto3
import traceback

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('serverless-database')
ses = boto3.client('ses', region_name='us-east-1')

MY_EMAIL = "itspatolusola@gmail.com"

def handler(event, context):
    if event.get('rawPath') == '/favicon.ico':
        return {'statusCode': 200, 'body': json.dumps('Ignored')}

    method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')

    if method == 'POST':
        try:
            raw_body = event.get('body', '{}')
            if event.get('isBase64Encoded', False):
                raw_body = base64.b64decode(raw_body).decode('utf-8')
            if not raw_body:
                raw_body = '{}'

            body = json.loads(raw_body)
            name = body.get('name', 'Anonymous')
            sender_email = body.get('email', 'No email provided')
            message = body.get('message', '')

            if not message.strip():
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Message cannot be empty'})
                }

            ses.send_email(
                Source=MY_EMAIL,
                Destination={'ToAddresses': [MY_EMAIL]},
                ReplyToAddresses=[sender_email] if '@' in sender_email else [],
                Message={
                    'Subject': {'Data': f"Portfolio Contact from {name}"},
                    'Body': {
                        'Text': {
                            'Data': f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message}"
                        }
                    }
                }
            )

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Email sent successfully!'})
            }

        except Exception:
            traceback.print_exc()
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to send email'})
            }

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