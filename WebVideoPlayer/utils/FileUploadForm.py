'''
Created on Oct 31, 2020

@author: duicul
'''
from django import forms

class FileUploadForm(forms.Form):
    folder = forms.CharField(max_length=50,label="Folder ")
    file = forms.FileField(label="Select a file to upload ")