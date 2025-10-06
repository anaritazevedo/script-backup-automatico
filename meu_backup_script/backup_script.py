import os
import shutil
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- CONFIGURAÇÕES ---
PASTA_A_COPIAR = 'C:/Users/Ana/Desktop/area' 
NOME_DO_BACKUP = 'backup_area'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def autenticar_google_drive():
    """Autentica com a API do Google Drive e retorna o serviço."""
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
    """Compacta uma pasta no formato .zip e retorna o caminho do arquivo."""
    print(f"Compactando a pasta '{caminho_pasta}'...")
    try:
        # shutil.make_archive cria o .zip, por isso não adicionamos a extensão no nome
        caminho_zip = shutil.make_archive(nome_arquivo_saida, 'zip', caminho_pasta)
        print(f"Pasta compactada com sucesso em: '{caminho_zip}'")
        return caminho_zip
    except Exception as e:
        print(f"ERRO ao compactar a pasta: {e}")
        return None

def upload_para_drive(service, arquivo):
    """Faz o upload de um arquivo para o Google Drive."""
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

def main():
    """Função principal que orquestra todo o processo de backup."""
    # Gera um nome de arquivo único com data e hora
    timestamp = datetime.now().strftime('%d_%m_%Y')
    nome_arquivo_zip_base = f"{NOME_DO_BACKUP}_{timestamp}"

    # 1. Compacta a pasta
    caminho_arquivo_compactado = compactar_pasta(PASTA_A_COPIAR, nome_arquivo_zip_base)
    
    # 2. Se a compactação funcionou, continua para o upload
    if caminho_arquivo_compactado:
        # 3. Autentica e obtém o serviço do Drive
        servico_drive = autenticar_google_drive()
        
        # 4. Faz o upload do arquivo
        upload_para_drive(servico_drive, caminho_arquivo_compactado)

        # 5. Remove o arquivo .zip local para economizar espaço
        print(f"Limpando arquivo zip local: '{caminho_arquivo_compactado}'...")
        os.remove(caminho_arquivo_compactado)
        print("Backup concluído e arquivo local removido. ✅")

# Ponto de entrada do script:
# Esta linha garante que a função main() só será executada quando você rodar o script diretamente.
if __name__ == '__main__':
    main()