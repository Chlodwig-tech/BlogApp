from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):

    username  = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email     = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)

    def validate_fields(self, valid_username=False, valid_email=False, valid_password=False):
        self.fields['username'].widget.attrs.update({'class':f'form-control is-{"" if valid_username else "in"}valid'})
        self.fields['email'].widget.attrs.update({'class':f'form-control is-{"" if valid_email else "in"}valid'})
        self.fields['password1'].widget.attrs.update({'class':f'form-control is-{"" if valid_password else "in"}valid'})
        self.fields['password2'].widget.attrs.update({'class':f'form-control is-{"" if valid_password else "in"}valid'})

        self.validate_fields_v = True

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)

    def validate_fields(self):
        self.fields['username'].widget.attrs.update({'class':f'form-control is-invalid'})
        self.fields['password'].widget.attrs.update({'class':f'form-control is-invalid'})

        self.validate_fields_v = True        