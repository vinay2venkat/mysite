from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate, login, logout, get_user_model


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    class Meta:
        model =User
        fields = ['username', 'email', 'password']

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password != password1:
            raise forms.ValidationError("Password and Confirm Password didn't match")
        return super(UserForm, self).clean(*args, **kwargs)




class UserLoginForm(forms.Form):
    username=forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
               raise forms.ValidationError("This user Does not exist")
            if not user.check_password(password):
               raise forms.ValidationError("TIncorrect Password")
            if not user.is_active:
               raise forms.ValidationError("This user is not longer active")
        return super(UserLoginForm, self).clean(*args, **kwargs)






