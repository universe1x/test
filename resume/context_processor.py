from .models import Resume

def resume_context(request):
    if request.user.is_authenticated and hasattr(request, 'session'):
        telegram_id = request.session.get('telegram_id')
        if telegram_id:
            try:
                resume = Resume.objects.get(telegram_user__telegram_id=telegram_id)
                return {'user_resume_id': resume.pk}
            except Resume.DoesNotExist:
                pass
    return {'user_resume_id': None}