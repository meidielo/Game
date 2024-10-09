from django import forms
# from game.models import Profile



class PersonalForm(forms.Form):

    username = forms.CharField(label="username", max_length = 100)
    # email = forms.CharField(label="email", max_length = 100)
    # phone_number = forms.CharField(label="phone", max_length = 100)
    password = forms.CharField(label="password", max_length = 100)
    confirm_password = forms.CharField(label="confirm_password", max_length = 100)
