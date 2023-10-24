import os
import sys
import logging
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from notifypy import Notify

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "service_account.json"
PARENT_FOLDER_ID = "1Eb7WWuP6Qdq-pZw3SmZZfvMmtlXMSL1e"





def setup_log(name):
    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    filename = f'./test_{name}.log'
    log_handler = logging.FileHandler(filename)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(log_format)

    logger.addHandler(log_handler)

    return logger

#Displays a visual notifier
def send_notification(title, description):
    notification = Notify(default_notification_title=str(title), default_notification_message=str(description))
    notification.send()

def write_log(name, message):
    logger = setup_log(name)
    logger.info(message) 

def validate_if_file_exists(file_path):
    #Check if given path exists
    file_exists = os.path.isfile(file_path)
    if not file_exists:
        send_notification("GDrive Upload", "File specified does not exist")
        write_log("execution_history", f'File specified does not exist {file_path}')
        sys.exit(f'File does not exists: {file_path}')
    
def get_filename_and_filename_with_suffix(input_file_path):
    try:
        #Split file_name from file_path without suffix
        file_name = Path(input_file_path).stem
        #Split file_name from file_path + suffix
        file_name_with_suffix = Path(input_file_path).name
        return file_name, file_name_with_suffix
    except Exception as e:
        write_log("execution_history", e)
        send_notification("GDrive Upload", "Error to split filenames")

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_file(file_path, filename, filename_with_suffix):
    try:
        #Try to estabilish connection to google api
        creds = authenticate()
        service = build("drive", "v3", credentials=creds)

        #Metadata to use when saving file
        file_metadata = {
            "name": filename,
            "parents": [PARENT_FOLDER_ID]
        }

        #Upload the file based on the metadata
        media = MediaFileUpload(file_path, 
                                mimetype="application/octet-stream")

        #Migrate the changes
        file = service.files().create(
            body = file_metadata,
            media_body = media,
        ).execute()

        send_notification("GDrive Upload", "Upload completed successful")
        write_log("execution_history", "file_response:")
        write_log("execution_history", file)
    except Exception as e:
        write_log("execution_history", e)
        send_notification("GDrive Upload", "Error to upload")
        

def delete_kdbx_files_and_empty_trash(filename):
    try:
        creds = authenticate()
        service = build("drive", "v3", credentials=creds)

        query = fr"name='{filename}'"

        list_response = service.files().list(
        orderBy   = "createdTime desc",
        q         = query,
        pageSize  = 22,
        fields    = "files(id, name)"
        ).execute()


        items = list_response.get("files", [])
        if items:
            for index, item in enumerate(items):
                ''' 
                    Skip index 0
                    Which means if the next upload fails or
                    not we will always have the most recent item 
                    matched in the cloud ,backed up
                '''
                if index > 0:
                    write_log("execution_history", "I will try to delete this file:")
                    write_log("execution_history", f'{item["name"]} ({item["id"]})')
                    del_response = service.files().delete(fileId=item["id"]).execute()
                    write_log("execution_history", "del_response:")
                    write_log("execution_history", del_response)
            
            #After finish putting files in the trash |  empties the trash
            write_log("execution_history", "I will try to emptyTrash:")
            trash_response = service.files().emptyTrash().execute()
            write_log("execution_history", "trash_response:")
            write_log("execution_history", trash_response)


        else:
            write_log("No matching files to be deleted found in your google-drive account.", "")
    except Exception as e:
            write_log("execution_history", e)
            send_notification("GDrive Upload", "Error cleaning the trash")






if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <file_path>")
        sys.exit()  

    input_file_path = sys.argv[1]
    write_log("execution_history", f'Starting script for {input_file_path}')

    #check if file exists
    validate_if_file_exists(input_file_path)

    filename, filename_with_suffix = get_filename_and_filename_with_suffix(input_file_path)

    # Parte que vou usar
    delete_kdbx_files_and_empty_trash(filename)
    upload_file(input_file_path, filename, filename_with_suffix)