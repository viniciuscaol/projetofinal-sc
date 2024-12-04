import boto3
import random
import os
from datetime import datetime

# Configuração do bucket S3
BUCKET_NAME = "s3-projetofinal-scaws"
REGION_NAME = "us-east-1"

# Inicializa o cliente S3
s3_client = boto3.client('s3', region_name=REGION_NAME)

def generate_file():
    filename = f"arquivo_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    num_lines = random.randint(5, 100)

    # Gera um arquivo com número aleatório de linhas
    with open(filename, 'w') as file:
        for i in range(num_lines):
            file.write(f"Linha {i + 1}\n")

    return filename

def upload_to_s3(filename):
    try:
        s3_client.upload_file(filename, BUCKET_NAME, filename)
        print(f"Arquivo {filename} enviado para o bucket {BUCKET_NAME} com sucesso!")
        os.remove(filename)  # Remove o arquivo local após o envio
    except Exception as e:
        print(f"Erro ao enviar arquivo: {str(e)}")

if __name__ == "__main__":
    filename = generate_file()
    upload_to_s3(filename)
