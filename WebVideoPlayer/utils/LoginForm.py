'''
Created on Oct 30, 2020

@author: duicul
'''
from django import forms


class LoginForm(forms.Form):
   username = forms.CharField(max_length = 100,label='username')
   password = forms.CharField(widget = forms.PasswordInput(),label='password')

   def clean_message(self):
       username = self.cleaned_data["username"]
       return username