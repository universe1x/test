from django.shortcuts import render, redirect
from .forms import TelegramLoginForm
from django.contrib import messages


def login(request):
    if request.method == 'POST':
        form = TelegramLoginForm(request.POST)
        if form.is_valid():
            # Получаем проверенные данные из формы
            telegram_id = form.cleaned_data['telegram_id']
            
            # Сохраняем telegram_id в сессии
            request.session['telegram_id'] = telegram_id
            
            # Можно добавить дополнительные данные в сессию, если нужно
            # request.session['user_name'] = form.cleaned_data['name']
            
            # Добавляем сообщение об успешном входе
            messages.success(request, 'Вы успешно вошли в систему')
            
            return redirect('group_list')  # или куда вам нужно после успешного входа
    else:
        form = TelegramLoginForm()
    
    return render(request, 'main/login.html', {'form': form})

   