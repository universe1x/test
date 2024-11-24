import logging
from django.contrib import messages
from django.shortcuts import redirect

logger = logging.getLogger(__name__)

class SessionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            telegram_id = request.session.get('telegram_id')
            if not telegram_id and request.path not in ['/login/', '/', '/logout/']:
                logger.warning(f"No telegram_id in session for authenticated user: {request.user}")
                messages.warning(request, 'Сессия истекла. Пожалуйста, войдите снова')
                return redirect('login')
        
        response = self.get_response(request)
        return response