'''
Created on Oct 28, 2020

@author: duicul
'''
from pathlib import Path
import os
import re
BASE_DIR = Path(__file__).resolve().parent.parent
#print(BASE_DIR)
def parse_dir(path):
    #print(path)
    t=[]
    main_path=path
    #print(main_path)
    exten = ['.mp4','.avi','.m3u8']
    for dirpath, dirnames, files in os.walk(path,followlinks=True):
        for name in files:
            for ext in exten:
                if name.lower().endswith(ext):
                    #print(name)
                    #print(dirpath)
                    #print(os.path.join(dirpath, name))
                    #t.append(os.path.join(dirpath, name))
                    out_path=os.path.join(dirpath, name)
                    #print(out_path)
                    #print(main_path)
                    #print(os.path.relpath(out_path,start=main_path))
                    #print(re.sub(r'^\.\\','',out_path))
                    #print()
                    main_moive_path=Path(out_path).resolve().parent.parent if ext == ".m3u8" else Path(out_path).resolve().parent
                    img_path=os.path.join(main_moive_path,"poster.jpg")
                    if not os.path.isfile(img_path):
                        img_path="/static/img/not_found.jpg"
                    else:
                        img_path="/media/"+os.path.relpath(img_path,start=main_path).replace("\\","/")
                    main_file_name=name.split(".")
                    main_file_name=''.join(main_file_name[0:len(main_file_name)-1])
                    #print(main_file_name)
                    #print(img_path)
                    new_entry={"name":main_file_name,"img_url":img_path,"movie_url":"/media/"+os.path.relpath(out_path,start=main_path).replace("\\","/")}
                    #print(new_entry)
                    t.append(new_entry)
    return t

def parse_media_dir():
    return parse_dir(os.path.join(BASE_DIR,'media'))
if __name__ == "__main__":
    out=parse_media_dir()
    print(out)