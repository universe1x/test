from django import forms
from .models import Resume, Ability

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['specialization', 'name', 'surname', 'phone', 'email', 'city', 'about']
        labels = {
            'specialization': 'Специализация',
            'name': 'Имя',
            'surname': 'Фамилия',
            'phone': 'Телефон',
            'email': 'Email',
            'city': 'Город',
            'about': 'О себе'
        }
        widgets = {
            'specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Frontend-разработчик'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя'
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите вашу фамилию'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 999-99-99'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@email.com'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Москва'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите о своем опыте работы и ключевых достижениях'
            })
        }

class AbilityForm(forms.Form):
    ability = forms.CharField(
        label='Навык',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: JavaScript'
        })
    )
    level = forms.ChoiceField(
        label='Уровень',
        choices=[
            ('начальный', 'Начальный'),
            ('средний', 'Средний'),
            ('высокий', 'Высокий')
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
