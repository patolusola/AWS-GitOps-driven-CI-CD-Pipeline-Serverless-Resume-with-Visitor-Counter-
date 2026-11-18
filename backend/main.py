import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('serverless-database')
ses = boto3.client('ses', region_name='us-east-1')

MY_EMAIL = "your.email@example.com"

def handler(event, context):
    # Ignore favicon requests
    if event.get('rawPath') == '/favicon.ico':
        return {'statusCode': 200, 'body': json.dumps('Ignored')}

    # Check if this is a Contact Form submission (POST) or Visitor Count (GET)
    method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')

    if method == 'POST':
        try:
            body = json.loads(event.get('body', '{}'))
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
        except Exception as e:
            print("SES Error:", str(e))
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to send email'})
            }

    # Default GET behavior: Visitor Counter
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