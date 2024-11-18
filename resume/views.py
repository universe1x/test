from django.shortcuts import render, redirect
from .forms import ResumeForm, AbilityForm
import json
from django.contrib import messages
from main.models import TelegramUser
from .models import Resume, Ability
from django.contrib.auth.decorators import login_required

@login_required
def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        ability_form = AbilityForm()
        
        if form.is_valid():
            resume = form.save(commit=False)
            telegram_id = request.session.get('telegram_id')
            try:
                telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
                resume.telegram_user = telegram_user
                resume.save()
                
                # Обработка навыков
                abilities = request.POST.get('abilities', '[]')
                try:
                    abilities_list = json.loads(abilities)
                    for ability_data in abilities_list:
                        if isinstance(ability_data, dict):
                            Ability.objects.create(
                                resume=resume,
                                name=ability_data.get('ability', ''),
                                level=ability_data.get('level', 'начальный')
                            )
                except json.JSONDecodeError:
                    pass
                
                return redirect('resume_detail', pk=resume.pk)
            except TelegramUser.DoesNotExist:
                messages.error(request, 'Пожалуйста, войдите в систему')
                return redirect('login')
    else:
        form = ResumeForm()
        ability_form = AbilityForm()
    
    return render(request, 'resume/create_resume.html', {
        'form': form,
        'ability_form': ability_form
    })

@login_required
def resume_detail(request, pk):
    try:
        telegram_id = request.session.get('telegram_id')
        telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
        resume = Resume.objects.get(pk=pk, telegram_user=telegram_user)
        return render(request, 'resume/resume_detail.html', {'resume': resume})
    except (Resume.DoesNotExist, TelegramUser.DoesNotExist):
        messages.error(request, 'Резюме не найдено')
        return redirect('create_resume')