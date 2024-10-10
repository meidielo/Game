from django import forms
# from game.models import Profile



class PersonalForm(forms.Form):

    username = forms.CharField(label="Username", max_length = 100)
    # email = forms.CharField(label="email", max_length = 100)
    # phone_number = forms.CharField(label="phone", max_length = 100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Confirm Password", max_length=100, widget=forms.PasswordInput())
    
    
