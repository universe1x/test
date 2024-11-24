from django.shortcuts import render, redirect
from .forms import ResumeForm, AbilityForm
import json
from django.contrib import messages
from main.models import TelegramUser
from .models import Resume, Ability
from django.contrib.auth.decorators import login_required

@login_required
def create_resume(request):
    # Сначала проверяем, есть ли уже резюме у пользователя
    telegram_id = request.session.get('telegram_id')
    try:
        telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
        existing_resume = Resume.objects.filter(telegram_user=telegram_user).first()
        
        if existing_resume:
            # Если резюме существует, перенаправляем на его просмотр
            return redirect('resume_detail', pk=existing_resume.pk)
            
        # Если резюме нет, продолжаем процесс создания
        if request.method == 'POST':
            form = ResumeForm(request.POST)
            ability_form = AbilityForm()
            
            if form.is_valid():
                resume = form.save(commit=False)
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
        else:
            form = ResumeForm()
            ability_form = AbilityForm()
        
        return render(request, 'resume/create_resume.html', {
            'form': form,
            'ability_form': ability_form
        })
        
    except TelegramUser.DoesNotExist:
        messages.error(request, 'Пожалуйста, войдите в систему')
        return redirect('login')

@login_required
def resume_detail(request, pk):
    try:
        telegram_id = request.session.get('telegram_id')
        telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
        resume = Resume.objects.get(pk=pk, telegram_user=telegram_user)
        abilities = Ability.objects.filter(resume=resume)
        
        context = {
            'resume': resume,
            'abilities': abilities
        }
        
        return render(request, 'resume/resume_detail.html', context)
        
    except (Resume.DoesNotExist, TelegramUser.DoesNotExist):
        messages.error(request, 'Резюме не найдено')
        return redirect('create_resume')
    except Exception as e:
        messages.error(request, f'Произошла ошибка: {str(e)}')
        return redirect('create_resume')
    
@login_required
def edit_resume(request, pk):
    try:
        telegram_id = request.session.get('telegram_id')
        telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
        resume = Resume.objects.get(pk=pk, telegram_user=telegram_user)
        abilities = Ability.objects.filter(resume=resume)
        
        if request.method == 'POST':
            # Обновляем основные поля резюме
            resume.name = request.POST.get('name')
            resume.surname = request.POST.get('surname')
            resume.city = request.POST.get('city')
            resume.email = request.POST.get('email')
            resume.phone = request.POST.get('phone')
            resume.about = request.POST.get('about')
            resume.additional_info = request.POST.get('additional_info')
            resume.save()
            
            # Удаляем старые навыки
            Ability.objects.filter(resume=resume).delete()
            
            # Добавляем новые навыки
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
            
            messages.success(request, 'Резюме успешно обновлено')
            return redirect('resume_detail', pk=resume.pk)
        
        return render(request, 'resume/edit_resume.html', {
            'resume': resume,
            'abilities': abilities
        })
        
    except (Resume.DoesNotExist, TelegramUser.DoesNotExist):
        messages.error(request, 'Резюме не найдено')
        return redirect('create_resume')
    except Exception as e:
        messages.error(request, f'Произошла ошибка: {str(e)}')
        return redirect('create_resume')