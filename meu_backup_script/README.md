# Script de Backup Automático para Google Drive

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)
![Status](https://img.shields.io/badge/status-funcional-brightgreen.svg?style=for-the-badge)

Um script de automação robusto e eficiente para realizar backups de diretórios locais diretamente no Google Drive, projetado para ser executado automaticamente na inicialização do Windows.

---

## 📜 Sobre o Projeto

A perda de dados locais é um risco constante para qualquer desenvolvedor ou usuário. Este projeto foi criado para mitigar esse risco, oferecendo uma solução "configure e esqueça" para backups. Utilizando o poder da API do Google Drive e do Agendador de Tarefas do Windows, o script garante que cópias de segurança de diretórios importantes sejam compactadas, datadas e enviadas para a nuvem de forma segura e periódica, sem intervenção manual.

## ✨ Funcionalidades Principais

-   🔄 **Automação Completa:** Executa automaticamente no logon do usuário via Agendador de Tarefas.
-   🗜️ **Compressão Eficiente:** Compacta a pasta de origem em um arquivo `.zip`, economizando espaço na nuvem.
-   📅 **Nomenclatura Inteligente:** Cada backup é nomeado com a data no formato `DD-MM-AAAA`, criando um histórico de versões claro e organizado.
-   🔐 **Autenticação Segura:** Implementa o fluxo OAuth 2.0 para uma autenticação segura com a API do Google, sem expor senhas.
-   🧹 **Limpeza Automática:** Após o upload bem-sucedido, o arquivo `.zip` local é removido para liberar espaço em disco.

## 🛠️ Tecnologias Utilizadas

| Tecnologia               | Propósito                                      |
| ------------------------ | ---------------------------------------------- |
| **Python 3** | Linguagem principal do script                  |
| **Google Drive API v3** | Para interagir com o armazenamento em nuvem    |
| **Google API Libraries** | `google-api-python-client`, `google-auth-oauthlib` |
| **Agendador de Tarefas** | Automação da execução no Windows               |
| **Git & GitHub** | Controle de versão e hospedagem do código      |

## 🏗️ Arquitetura e Fluxo de Execução

O processo é orquestrado para ser simples e resiliente:

```
1. Logon do Usuário no Windows
   └──> 2. Agendador de Tarefas aciona o 'iniciar_backup.bat'
        └──> 3. O .bat define o diretório correto e executa 'backup_script.py'
             └──> 4. O Script Python:
                  ├── a. Autentica com o Google Drive (usando 'token.json')
                  ├── b. Compacta o diretório local alvo
                  ├── c. Faz o upload do arquivo .zip
                  └── d. Remove o arquivo .zip local
```

> **Nota:** Na primeira execução, o fluxo de autenticação (passo 4a) irá abrir um navegador para que o usuário conceda as permissões necessárias, criando o arquivo `token.json` para as futuras execuções.

## 🚀 Começando

Para colocar este projeto em funcionamento no seu ambiente, siga os passos abaixo.

### Pré-requisitos

-   Python 3.9 ou superior
-   Git
-   Uma Conta Google

### Instalação e Configuração

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/anaritazevedo/script-backup-automatico.git](https://github.com/anaritazevedo/script-backup-automatico.git)
    cd script-backup-automatico
    ```

2.  **Instale as dependências a partir do `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure as Credenciais da API do Google:**
    -   Siga o [guia oficial do Google](https://developers.google.com/workspace/guides/create-credentials) para criar um **ID do cliente OAuth** para um **"Aplicativo para computador"**.
    -   Faça o download do arquivo de credenciais.
    -   **Importante:** Renomeie o arquivo para `credentials.json` e coloque-o na raiz deste projeto. Este arquivo é pessoal e intransferível (já está no `.gitignore`).

4.  **Configure o Script:**
    -   Abra o arquivo `backup_script.py`.
    -   Altere a variável `PASTA_A_COPIAR` para o caminho absoluto da pasta que você deseja fazer backup.
        ```python
        PASTA_A_COPIAR = 'C:/caminho/completo/para/sua/pasta'
        ```

##  kullanım Uso

### Primeira Execução Manual

Para autorizar o acesso à sua conta, a primeira execução deve ser manual:
```bash
python backup_script.py
```
Siga as instruções no navegador que será aberto para conceder as permissões.

### Configurando a Automação

Utilize o Agendador de Tarefas do Windows para executar o `iniciar_backup.bat` no logon do usuário. Siga o guia [neste link](https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10) ou use os passos simplificados no `README` anterior.

## 🤝 Como Contribuir

Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será **muito apreciada**.

1.  Faça um Fork do Projeto
2.  Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Faça o Commit de suas alterações (`git commit -m 'Add some AmazingFeature'`)
4.  Faça o Push para a Branch (`git push origin feature/AmazingFeature`)
5.  Abra um Pull Request

## ⚖️ Licença

Distribuído sob a Licença MIT. Veja `LICENSE.txt` para mais informações.

## 👤 Autora

**Ana Rita Azevedo**

-   [GitHub: @anaritazevedo](https://github.com/anaritazevedo)
-   [Linkedin: anaritazevedo](https://www.linkedin.com/in/anaritazevedo/)

-   Sinta-se à vontade para entrar em contato!

--- 