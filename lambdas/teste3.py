def lambda_handler(event, context):
    name = event.get('name')  

    if not name:
        return {
            'statusCode': 400,
            'body': 'Error: "name" o parametro name é requerido.'
        }

    return {
        'statusCode': 200,
        'body': f'Hello, {name}! Welcome to AWS Lambda.'
    }