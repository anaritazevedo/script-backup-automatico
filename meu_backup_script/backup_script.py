import os
import shutil
from datetime import datetime
import configparser 
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

def autenticar_google_drive():
    print("Autenticando com o Google Drive...")
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
    
    print("Autenticação bem-sucedida.")
    return build('drive', 'v3', credentials=creds)

def compactar_pasta(caminho_pasta, nome_arquivo_saida):
    print(f"Compactando a pasta '{caminho_pasta}'...")
    try:
        caminho_zip = shutil.make_archive(nome_arquivo_saida, 'zip', caminho_pasta)
        print(f"Pasta compactada com sucesso em: '{caminho_zip}'")
        return caminho_zip
    except Exception as e:
        print(f"ERRO ao compactar a pasta: {e}")
        return None

def upload_para_drive(service, arquivo):
    print(f"Iniciando upload do arquivo '{arquivo}'...")
    file_metadata = {'name': os.path.basename(arquivo)}
    media = MediaFileUpload(arquivo, resumable=True)
    
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Upload concluído! Arquivo enviado com ID: {file.get('id')}")
        return file.get('id')
    except Exception as e:
        print(f"ERRO ao enviar arquivo '{arquivo}': {e}")
        return None

def limpar_backups_antigos(service, nome_base_backup):
    print("Procurando por backups antigos para limpar...")
    
    try:
        query = f"name contains '{nome_base_backup}' and trashed = false"
        response = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, createdTime)'
        ).execute()
        files = response.get('files', [])

        if len(files) > 1:
            files.sort(key=lambda x: x['createdTime'], reverse=True)
            
            arquivos_para_deletar = files[1:]
            print(f"Encontrados {len(arquivos_para_deletar)} backups antigos para remover.")

            for file in arquivos_para_deletar:
                file_id = file.get('id')
                file_name = file.get('name')
                print(f"  - Deletando '{file_name}'...")
                service.files().delete(fileId=file_id).execute()
            
            print("Limpeza de backups antigos concluída.")
        else:
            print("Nenhum backup antigo para limpar.")

    except Exception as e:
        print(f"ERRO durante a limpeza de backups antigos: {e}")

def main():
    timestamp = datetime.now().strftime('%d-%m-%Y')
    nome_arquivo_zip_base = f"{NOME_DO_BACKUP}_{timestamp}"

    caminho_arquivo_compactado = compactar_pasta(PASTA_A_COPIAR, nome_arquivo_zip_base)
    
    if caminho_arquivo_compactado:
        servico_drive = autenticar_google_drive()
        
        id_arquivo_novo = upload_para_drive(servico_drive, caminho_arquivo_compactado)

        if id_arquivo_novo:
            limpar_backups_antigos(servico_drive, NOME_DO_BACKUP)

        print(f"Limpando arquivo zip local: '{caminho_arquivo_compactado}'...")
        os.remove(caminho_arquivo_compactado)
        print("Processo de backup concluído e arquivo zip local removido. ✅")

if __name__ == '__main__':
    main()