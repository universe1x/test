from django.shortcuts import render, redirect
from .forms import GroupForm
from .models import Group
from main.models import TelegramUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        
        if form.is_valid():
            group = form.save(commit=False)
            telegram_id = request.session.get('telegram_id')
            try:
                telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
                group.telegram_user = telegram_user
                group.save()
                return redirect('group_list')
            except TelegramUser.DoesNotExist:
                return redirect('login')

    else:
        form = GroupForm()
    return render(request, 'groups/create_group.html', {'form': form})

@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'groups/group_list.html', {'groups': groups})

@login_required
def group_detail(request):
    try:
        telegram_id = request.session.get('telegram_id')
        telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
        
        # Проверяем, есть ли у пользователя группа
        existing_group = Group.objects.filter(telegram_user=telegram_user).first()
        
        if existing_group:
            # Если группа есть, показываем детали группы
            return render(request, 'groups/group_detail.html', {'group': existing_group})
        else:
            # Если группы нет, показываем форму создания
            if request.method == 'POST':
                form = GroupForm(request.POST)
                if form.is_valid():
                    group = form.save(commit=False)
                    group.telegram_user = telegram_user
                    group.save()
                    return redirect('group_detail')
            else:
                form = GroupForm()
            return render(request, 'groups/create_group.html', {'form': form})
            
    except TelegramUser.DoesNotExist:
        return redirect('login')

@login_required
def group_view(request, pk):
    try:
        telegram_id = request.session.get('telegram_id')
        telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
        
        # Получаем группу по pk и проверяем, что это не группа текущего пользователя
        group = get_object_or_404(Group, pk=pk)
        
        # Если пользователь пытается просмотреть свою группу, перенаправляем на group_detail
        if group.telegram_user == telegram_user:
            return redirect('group_detail')
            
        return render(request, 'groups/group_view.html', {
            'group': group,
            'is_owner': False
        })
        
    except TelegramUser.DoesNotExist:
        return redirect('login')

@login_required
def edit_group(request):
    try:
        telegram_id = request.session.get('telegram_id')
        telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
        group = Group.objects.get(telegram_user=telegram_user)
        
        if request.method == 'POST':
            form = GroupForm(request.POST, instance=group)
            if form.is_valid():
                form.save()
                return redirect('group_detail')
        else:
            form = GroupForm(instance=group)
            
        return render(request, 'groups/edit_group.html', {
            'form': form,
            'group': group
        })
        
    except (TelegramUser.DoesNotExist, Group.DoesNotExist):
        return redirect('group_detail')

@login_required
def delete_group(request):
    telegram_id = request.session.get('telegram_id')
    telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
    group = Group.objects.get(telegram_user=telegram_user)
    group.delete()
    return redirect('group_detail')


