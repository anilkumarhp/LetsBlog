from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Post
from django import forms
from taggit.managers import TaggableManager


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}),)
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),)
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Conform Password'


class NewPost(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-4 w-50', 'placeholder': 'Title'}),)
    editor1 = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control w-100 mb-4'}),)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-4 w-50', 'placeholder': 'A comma-separated list of tags.'}),)

    class Meta:
        model = Post
        fields = ('title', 'editor1', 'tags', 'status')

    def __init__(self, *args, **kwargs):
        super(NewPost, self).__init__(*args, **kwargs)


class SearchForm(forms.Form):
    query = forms.CharField()


class PasswordReset(PasswordResetForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Email ID"}),)

    class Meta:
        model = User
        fields = 'email'
