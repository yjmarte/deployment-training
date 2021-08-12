from django import forms
from .models import *

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", max_length=255, required=False)
    last_name = forms.CharField(label="Last Name", max_length=255, required=False)
    email = forms.EmailField(label="Email Address", required=False)
    password = forms.CharField(max_length=255, required=False, widget=forms.PasswordInput)
    c_password = forms.CharField(label="Confirm Password", max_length=255, required=False, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Setting class 'form-control' to all visible fields
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class LoginForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    password = forms.CharField(max_length=255, required=False, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("email", "password")
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # Setting class 'form-control' to all visible fields
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class BookForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=False)
    description = forms.CharField(widget=forms.Textarea, max_length=255, required=False)
    
    class Meta:
        model = Book
        fields = ("title", "description")

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        # Setting class 'form-control' to all visible fields
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
