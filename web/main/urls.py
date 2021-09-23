from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView
from .views import SetUserTimeZone, TemplateAPIView


urlpatterns = [
    path('', TemplateAPIView.as_view(template_name='chat/index.html'), name='chat'),
    path('timezone/', SetUserTimeZone.as_view(), name='set_user_timezone'),

]
