'''
Created on Oct 31, 2020

@author: duicul
'''
import os 
import zipfile
from WebVideoPlayer.settings import BASE_DIR
import logging
logger = logging.getLogger("django")
def handle_uploaded_file(file,file_folder):
    media_upload_dir=os.path.join(BASE_DIR,"media_upload")
    try:
        os.mkdir(media_upload_dir)
    except FileExistsError:
        pass
    if(file.name.endswith(".zip")):
        upload_folder=os.path.join(BASE_DIR,"media")
        upload_folder=os.path.join(upload_folder,file_folder)
        
    else:
        upload_folder=os.path.join(media_upload_dir,file_folder)
    logger.info("upload folder path : "+str(upload_folder))
    try:
        os.mkdir(upload_folder)
    except FileExistsError:
        pass
    with open(os.path.join(upload_folder,file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    
    if(file.name.endswith(".zip")):       
            with zipfile.ZipFile(os.path.join(upload_folder,file.name), 'r') as zip_ref:
                zip_ref.extractall(upload_folder)
    
    