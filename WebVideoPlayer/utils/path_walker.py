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
    exten = ['.mp4','.avi','.m3u8']
    for dirpath, dirnames, files in os.walk(path,followlinks=True):
        for name in files:
            for ext in exten:
                if name.lower().endswith(ext):
                    #print(name)
                    print(dirpath)
                    #print(os.path.join(dirpath, name))
                    #t.append(os.path.join(dirpath, name))
                    out_path=os.path.join(dirpath, name)
                    #print(out_path)
                    #print(main_path)
                    #print(os.path.relpath(out_path,start=main_path))
                    #print(re.sub(r'^\.\\','',out_path))
                    #print()
                    t.append([re.sub(r'^\.\\','',out_path),os.path.relpath(out_path,start=main_path)])
    return t

def parse_media_dir():
    return parse_dir(os.path.join(BASE_DIR,'media'))
if __name__ == "__main__":
    out=parse_media_dir()
    print(out)