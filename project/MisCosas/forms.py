from django import forms

class LoginForm(forms.Form):
    Username = forms.CharField()
    Password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    Username = forms.CharField()
    Email = forms.EmailField()
    Password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    image = forms.ImageField()

class changePhoto(forms.Form):
    image = forms.ImageField()

"""
class YoutubeForm(forms.Form):
    id = forms.CharField()
    
class Reddit(forms.Form):
    Section = forms.CharField()
   
class LastFmForm(forms.Form):
"""