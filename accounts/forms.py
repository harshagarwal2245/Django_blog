from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput,max_length=16, min_length=8)


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100,)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput,max_length=16, min_length=8)
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput,max_length=16, min_length=8)
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    class Meta:
        model = User 
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data    


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'date_of_birth', 'experience']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email']