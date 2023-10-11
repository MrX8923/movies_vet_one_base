from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MyMailField(forms.EmailField):
    def __init__(self, **kwargs):
        super(MyMailField, self).__init__(**kwargs)
        self.required = True
        self.strip = True


class SingUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')
        field_classes = {'email': MyMailField}
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'arkasha2000'}),
            'password1': forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                                    'placeholder': '********'}),
            'password2': forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                                    'placeholder': '********'}),
            'email': forms.EmailInput(attrs={'placeholder': 'arkasha@mail.ru'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Аркадий'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Аркадьев'})
        }
