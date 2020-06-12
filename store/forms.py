from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        help_texts = {
        'username' : None,
        'password1': None,
        'password2': None,
        }

    def __init__(self,*args,**kwargs):
        super(UserRegistrationForm,self).__init__(*args,**kwargs)
        self.fields['username'].label = 'UserName'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter User Name'
        self.fields['email'].label = 'Email'
        self.fields['email'].widget.attrs['placeholder'] = "Enter Email Address"
        self.fields['password1'].label = 'Password'
        self.fields['password1'].widget.attrs['password1'] = 'Enter Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].widget.attrs['password2'] = 'Re-Confirm Your Password'
