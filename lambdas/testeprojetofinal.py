import json
import boto3
import os

sqs = boto3.client('sqs')
sns = boto3.client('sns')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Obter o arquivo do S3
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        
        # Contar linhas
        line_count = len(file_content.splitlines())
        
        # Armazenar informações
        file_info = {
            'file_name': key,
            'line_count': line_count,
            'date': str(context.aws_request_id)  # ou use datetime para a data atual
        }
        
        # Enviar mensagem para SQS
        sqs.send_message(
            QueueUrl=os.environ['https://sqs.us-east-1.amazonaws.com/434876288613/sqs-projetofinal-scaws'],
            MessageBody=json.dumps(file_info)
        )
        
        # Publicar no SNS
        sns.publish(
            TopicArn=os.environ['arn:aws:sns:us-east-1:434876288613:sns-projetofinal-scaws'],
            Message=json.dumps(file_info)
        )
        
    return {
        'statusCode': 200,
        'body': json.dumps('Processamento concluído com sucesso!')
    }