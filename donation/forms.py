from django import forms
from .models import Challenges, UserProfile, ChallengesComments
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout, login
import string
from taggit.forms import *
from django.forms.widgets import ClearableFileInput


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=4, max_length=150)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError('Email already exists')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password don\'t match')
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        # user.active = False # Send confirmation Email
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=2, max_length=15, required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=2, max_length=25, required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'last_name',)


class UserProfileEditForm(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'data-length': '150', 'cols': '10', 'rows': '2'}), required=False)
    profile_photo = forms.ImageField(required=False)
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = UserProfile
        fields = ('about', 'profile_photo', 'phone',)


class LogInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password',)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_name = User.objects.filter(email=username).values('username')

        if user_name:
            email = user_name[0]['username']
            user = authenticate(username=email, password=password)
        else:
            user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_name = User.objects.filter(email=username).values('username')
        if user_name:
            email = user_name[0]['username']
            user = authenticate(username=email, password=password)
        else:
            user = authenticate(username=username, password=password)
        return user


class CreateChallengeForm(forms.ModelForm):
    about = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'data-length': '1000', 'cols': '10', 'rows': '2'}))
    price_goal = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}))
    tags = TagField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Challenges
        fields = ('about',
                  'price_goal',
                  'tags',)

    def clean(self):
        cleaned_data = super(CreateChallengeForm, self).clean()
        price_goal = self.cleaned_data.get('price_goal')

        if int(price_goal) <= 0:
            msg = "Enter correct goal"
            self.add_error('price_goal', msg)
            

class UploadProofFile(forms.ModelForm):
    proof_img = forms.ImageField(required=False)

    class Meta:
        model = Challenges
        fields = ('proof_img',)


class ChallengeCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control bg-transparent text-light', 'placeholder': 'Comment . . .', 'data-length': '150', 'cols': '10', 'rows': '2'}), required=True)

    class Meta:
        model = ChallengesComments
        fields = ('comment', )

    def clean_email(self):
        comment = self.cleaned_data['comment']

        if comment == "":
            raise forms.ValidationError('The comment can\'t be empty')
        return comment
