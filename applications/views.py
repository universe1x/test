from django.shortcuts import render, redirect, get_object_or_404
from .models import Application
from groups.models import Group
from resume.models import Resume
from main.models import TelegramUser
from django.contrib.auth.decorators import login_required

@login_required
def create_application(request, group_id):
    try:
        # Получаем telegram_id из сессии
        telegram_id = request.session.get('telegram_id')
        
        if not telegram_id:
            return redirect('login')
            
        # Получаем пользователя по telegram_id
        telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
        
        # Получаем группу, в которую подается заявка
        group = get_object_or_404(Group, pk=group_id)
        
        # Проверяем, не является ли пользователь владельцем группы
        if group.telegram_user == telegram_user:
            return redirect('group_detail')
        
        try:
            # Получаем резюме пользователя
            resume = Resume.objects.get(telegram_user=telegram_user)
            
            if request.method == 'POST':
                # Проверяем, не существует ли уже заявка
                if not Application.objects.filter(group=group, resume=resume).exists():
                    # Создаем заявку
                    Application.objects.create(
                        group=group,
                        resume=resume
                    )
                    return redirect('application_success')
                else:
                    # Если заявка уже существует
                    return render(request, 'applications/create_application.html', {
                        'error': 'Вы уже отправили заявку в эту группу'
                    })
                    
            return render(request, 'applications/create_application.html', {
                'group': group
            })
            
        except Resume.DoesNotExist:
            return redirect('create_resume')
            
    except TelegramUser.DoesNotExist:
        return redirect('login')
