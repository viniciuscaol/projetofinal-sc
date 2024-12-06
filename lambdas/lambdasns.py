import json
import boto3

# Inicializa o cliente SNS
sns = boto3.client('sns')

# Número de telefone para o qual o SMS será enviado
cel = "+5571999573945"  # Substitua pelo número de telefone desejado

def lambda_handler(event, context):
    for record in event['Records']:
        # Extrai o corpo da mensagem
        message_body = json.loads(record['body'])
        filename = message_body['filename']
        line_count = message_body['countline']

        # Cria a mensagem SMS
        sms_message = f"O arquivo '{filename}' contém {line_count} linhas."

        try:
            # Envia o SMS
            response = sns.publish(
                PhoneNumber=cel,
                Message=sms_message
            )
            print(f"SMS enviado: {response.get('MessageId')}")
        except Exception as e:
            print(f"Erro ao enviar SMS: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Processamento concluído com sucesso.')
    }