from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'skills', 'link', 'specialization', 'location']
        labels = {
            'name': 'Название группы',
            'description': 'Описание',
            'skills': 'Требуемые навыки',
            'link': 'Ссылка на группу',
            'specialization': 'Специализация',
            'location': 'Местоположение'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Python разработчики'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Опишите вашу группу'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Например: Python, Django, PostgreSQL'
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://t.me/your_group'
            }),
            'specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Backend разработка'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Москва'
            })
        }
    