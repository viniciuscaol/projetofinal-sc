def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': '{"message": "Hello from Lambda via API Gateway!"}'
    }