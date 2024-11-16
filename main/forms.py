from django import forms
from .models import TelegramUser

class TelegramLoginForm(forms.Form):
    telegram_id = forms.CharField(
        label='Telegram ID',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш Telegram ID'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш пароль'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        telegram_id = cleaned_data.get('telegram_id')
        password = cleaned_data.get('password')

        if telegram_id and password:
            try:
                user = TelegramUser.objects.get(telegram_id=telegram_id)
                if user.password != password:
                    raise forms.ValidationError('Неверный пароль')
            except TelegramUser.DoesNotExist:
                raise forms.ValidationError('Пользователь с таким Telegram ID не найден')

        return cleaned_data
