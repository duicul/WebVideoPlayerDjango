'''
Created on Oct 31, 2020

@author: duicul
'''
import os 

from WebVideoPlayer.settings import BASE_DIR
def handle_uploaded_file(file,file_folder):
    media_upload_dir=os.path.join(BASE_DIR,"media_upload")
    try:
        os.mkdir(media_upload_dir)
    except FileExistsError:
        pass
    upload_folder=os.path.join(media_upload_dir,file_folder)
    try:
        os.mkdir(upload_folder)
    except FileExistsError:
        pass
    with open(os.path.join(upload_folder,file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)