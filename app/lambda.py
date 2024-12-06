import boto3
import zipfile
import io

# Configurações da função Lambda
function_name = "lambdas3"
runtime = "python3.13"
role_arn = "arn:aws:iam::434876288613:role/ProjetoFinal"
handler = "lambda_function.lambda_handler"

# Código da função Lambda
lambda_code = """
import json
import boto3
import urllib.parse
from datetime import datetime
import os

# Nome da tabela DynamoDB
DYNAMODB_TABLE = "contabilidade"
# URL da fila SQS
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/434876288613/sqs-projetofinal-scaws"
# Região da AWS
AWS_REGION = "us-east-1"

# Inicializa o cliente do DynamoDB, S3, SQS e SNS
dynamo = boto3.resource('dynamodb', region_name=AWS_REGION)
s3 = boto3.client('s3')
sqs = boto3.client('sqs', region_name=AWS_REGION)
table = dynamo.Table(DYNAMODB_TABLE)

def lambda_handler(event, context):
    # Processa cada registro no evento S3
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')

        try:
            # Obtém o objeto do S3
            response = s3.get_object(Bucket=bucket, Key=key)
            # Lê o conteúdo do arquivo
            file_content = response['Body'].read().decode('utf-8')
            # Conta as linhas do arquivo
            line_count = len(file_content.splitlines())

            # Gera um ID baseado na data e hora atuais
            id = datetime.now().strftime("%d%m%Y%H%M%S")  # Formato: AAAAMMDDHHMMSS

            # Salva o nome do arquivo e a contagem de linhas no DynamoDB
            table.put_item(
                Item={
                    'id': id,  # Usando a data e hora como ID
                    'filename': key,
                    'countline': line_count
                }
            )

            # Envia uma mensagem para a fila SQS
            message_body = json.dumps({
                'filename': key,
                'countline': line_count
            })
            sqs.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=message_body
            )

            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Item adicionado com sucesso", "filename": key, "countline": line_count})
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"message": f"Erro ao processar o arquivo: {str(e)}"})
            }
"""

# Criação de um arquivo ZIP com o código
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('lambda_function.py', lambda_code)
zip_buffer.seek(0)

# Conexão com o serviço Lambda
lambda_client = boto3.client('lambda')

# Criando a função Lambda
try:
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime=runtime,
        Role=role_arn,
        Handler=handler,
        Code={'ZipFile': zip_buffer.read()},
        Description='Minha primeira função Lambda criada com boto3',
        Timeout=10,  # Tempo máximo de execução em segundos
        MemorySize=128,  # Memória em MB
    )
    print("Função Lambda criada com sucesso!")
    print("Arn:", response['FunctionArn'])
except Exception as e:
    print("Erro ao criar a função Lambda:", e)