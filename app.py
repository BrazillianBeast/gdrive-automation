import sys
import logging
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'
PARENT_FOLDER_ID = "1Eb7WWuP6Qdq-pZw3SmZZfvMmtlXMSL1e"

def setup_log(name):
    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    filename = f"./test_{name}.log"
    log_handler = logging.FileHandler(filename)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(log_format)

    logger.addHandler(log_handler)

    return logger


def write_log(name, message):
    logger = setup_log(name)
    logger.info(message) 

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_file(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': 'Yolo',
        'parents': [PARENT_FOLDER_ID]
    }

    media = MediaFileUpload('mytest.kdbx', 
                            mimetype='application/octet-stream')

    file = service.files().create(
        body = file_metadata,
        media_body = media,
    ).execute()

    write_log('execution_history', 'file_response:')
    write_log('execution_history', file)

def delete_kdbx_files_and_empty_trash():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    list_response = service.files().list(
    orderBy   = "createdTime desc",
    q         = f"name='Yolo'",
    pageSize  = 22,
    fields    = "files(id, name)"
    ).execute()


    items = list_response.get('files', [])
    if items:
        for item in items:
            write_log('execution_history', 'I will try to delete this file:')
            write_log('execution_history', f'{item["name"]} ({item["id"]})')
            del_response = service.files().delete(fileId=item['id']).execute()
            write_log('execution_history', 'del_response:')
            write_log('execution_history', del_response)
        
        write_log('I will try to emptyTrash:')
        trash_response = service.files().emptyTrash().execute()
        write_log('execution_history', 'trash_response:')
        write_log('execution_history', trash_response)


    else:
        write_log('No matching files to be deleted found in your google-drive account.')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <kdbx_file_path>")
        sys.exit()
        
    input_path = sys.argv[1]
    write_log("execution_history", f"Starting script for {input_path}")

    # Parte que vou usar
    # delete_kdbx_files_and_empty_trash()
    # upload_file('mytest.kdbx')