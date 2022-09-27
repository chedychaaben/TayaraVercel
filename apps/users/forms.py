from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import Account as User

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.CharField(label='Adresse e-mail:',widget=forms.TextInput(attrs={'placeholder': 'Adresse e-mail','class':'form-control'}))
    password = forms.CharField(label='Mot de Passe:', widget=forms.PasswordInput(attrs={'placeholder': 'Mot de Passe','class':'form-control'})) # Pass hiding

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email , password=password)
            if not user and User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email ou mot de passe est incorrect.")  #"Incorrect Password."
            
            if not user:
                raise forms.ValidationError("Email ou mot de passe est incorrect.")  #"Incorrect Username."

        return super(UserLoginForm,self).clean(*args,**kwargs)