'''
Created on Oct 31, 2020

@author: duicul
'''
from django import forms


class ChunckFileUploadForm(forms.Form):
    filename = forms.CharField(max_length=200,label="FileName ")
    path = forms.CharField(max_length=200,label="FilePath ")
    file = forms.FileField(label="Select a file to upload ")