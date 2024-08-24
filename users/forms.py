from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailInput

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:  # Класс формы для модели User.
        model = User  # Модель для которой формируется форма.
        fields = ('email', 'password1', 'password2')


class PasswordResetForm(StyleFormMixin, forms.Form):
    email = forms.EmailField(
        label='Введите ваш email',
        max_length=254,
        required=True,
        widget=EmailInput(
            attrs={
                'placeholder': 'Введите адрес электронной почты',
                'class': 'form-control text-center',
            }
        ))
