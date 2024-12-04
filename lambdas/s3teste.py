import json
import boto3
import os

def lambda_handler(event, context):
    """
    Função Lambda que processa eventos do S3 (ObjectCreated e ObjectRemoved)
    e envia mensagens para uma fila SQS com o tipo do evento e a chave do objeto.
    """
    try:
        # Inicializa o cliente SQS
        sqs = boto3.client('sqs')
        
        # Obtém a URL da fila SQS da variável de ambiente
        queue_url = 'https://sqs.us-east-1.amazonaws.com/434876288613/atividade'
        
        # Processa os registros de eventos do S3
        for record in event['Records']:
            # Obtém as informações do bucket e objeto do S3
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']
            
            # Determina o tipo do evento
            event_name = record['eventName']
            action_type = 'CRIADO' if 'ObjectCreated' in event_name else 'REMOVIDO'
            
            # Prepara o payload da mensagem
            message = {
                'tipoAcao': action_type,
                'nomeObjeto': object_key,
                'nomeBucket': bucket_name
            }
            
            # Envia mensagem para o SQS
            response = sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message)
            )
            
            print(f"Mensagem enviada para o SQS. ID da Mensagem: {response['MessageId']}")
            
        return {
            'statusCode': 200,
            'body': json.dumps('Eventos processados com sucesso')
        }
        
    except Exception as e:
        print(f"Erro ao processar eventos: {str(e)}")
        raise e

# import boto3

# def lambda_handler(event, context):
#     # Detalhes do evento S3
#     bucket_name = event['Records'][0]['s3']['bucket']['name']
#     object_key = event['Records'][0]['s3']['object']['key']
    
#     print(f"Arquivo carregado no bucket {bucket_name}: {object_key}")
    
#     # Exemplo: Baixar o arquivo
#     s3 = boto3.client('s3')
#     local_path = f"/tmp/{object_key.split('/')[-1]}"
#     s3.download_file(bucket_name, object_key, local_path)
    
#     return {
#         'statusCode': 200,
#         'body': f"Processado o arquivo {object_key}"
#     }