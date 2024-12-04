def lambda_handler(event, context):
    name = event.get('name', 'ADA')  
    return {
        'statusCode': 200,
        'body': f'Hello, {name}! Welcome to AWS Lambda.'
    }