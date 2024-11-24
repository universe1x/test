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
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    return render(request, 'groups/group_detail.html', {'group': group})