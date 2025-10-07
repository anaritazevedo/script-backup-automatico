import os
import shutil
from datetime import datetime
import configparser 
import logging
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- CONFIGURAÇÕES ---
config = configparser.ConfigParser()
config.read('config.ini')

PASTA_A_COPIAR = config.get('Backup', 'pasta_a_copiar')
NOME_DO_BACKUP = config.get('Backup', 'nome_do_backup')

SCOPES = ['https://www.googleapis.com/auth/drive.file']


logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('backup.log', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
file_handler.setFormatter(file_formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_formatter = logging.Formatter('%(message)s') 
console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def autenticar_google_drive():
    logging.info("Autenticando com o Google Drive...")
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    logging.info("Autenticação bem-sucedida.")
    return build('drive', 'v3', credentials=creds)

def compactar_pasta(caminho_pasta, nome_arquivo_saida):
    logging.info(f"Zipando backup da pasta '{caminho_pasta}'...")
    try:
        caminho_zip = shutil.make_archive(nome_arquivo_saida, 'zip', caminho_pasta)
        return caminho_zip
    except Exception as e:
        logging.error(f"Falha ao compactar a pasta: {e}")
        return None

def upload_para_drive(service, arquivo):
    logging.info(f"Fazendo upload do backup '{os.path.basename(arquivo)}'...")
    file_metadata = {'name': os.path.basename(arquivo)}
    media = MediaFileUpload(arquivo, resumable=True)
    
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        logging.info("Upload realizado com sucesso!")
        return file.get('id')
    except Exception as e:
        logging.error(f"Falha ao enviar arquivo: {e}")
        return None

def limpar_backups_antigos(service, nome_base_backup):
    try:
        query = f"name contains '{nome_base_backup}' and trashed = false"
        response = service.files().list(q=query, spaces='drive', fields='files(id, name, createdTime)').execute()
        files = response.get('files', [])

        if len(files) > 1:
            files.sort(key=lambda x: x['createdTime'], reverse=True)
            arquivos_para_deletar = files[1:]
            
            for file in arquivos_para_deletar:
                file_id, file_name = file.get('id'), file.get('name')
                logging.info(f"Deletando o arquivo zipado antigo do Drive: '{file_name}'...")
                service.files().delete(fileId=file_id).execute()
                logging.info("Arquivo antigo do Drive deletado.")
        else:
            logging.info("Nenhum backup antigo encontrado no Drive para limpar.")

    except Exception as e:
        logging.error(f"Falha durante a limpeza de backups antigos: {e}")

def main():
    logging.info("\n--- INICIANDO PROCESSO DE BACKUP ---")
    timestamp = datetime.now().strftime('%d-%m-%Y')
    nome_arquivo_zip_base = f"{NOME_DO_BACKUP}_{timestamp}"

    caminho_arquivo_compactado = compactar_pasta(PASTA_A_COPIAR, nome_arquivo_zip_base)
    
    if caminho_arquivo_compactado:
        servico_drive = autenticar_google_drive()
        id_arquivo_novo = upload_para_drive(servico_drive, caminho_arquivo_compactado)

        if id_arquivo_novo:
            limpar_backups_antigos(servico_drive, NOME_DO_BACKUP)

        logging.info(f"Deletando o arquivo zipado localmente: '{caminho_arquivo_compactado}'...")
        os.remove(caminho_arquivo_compactado)
        logging.info("Arquivo zipado localmente deletado.")
        logging.info("--- PROCESSO DE BACKUP CONCLUÍDO ---")
    else:
        logging.error("--- PROCESSO DE BACKUP FALHOU NA ETAPA DE COMPACTAÇÃO ---")

if __name__ == '__main__':
    main()