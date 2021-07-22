from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from .views import *

app_name = 'users'

urlpatterns = [
    path('sign_in', LoginView.as_view(template_name='users/sign_in.html'), name='sign_in'),
    path('sign_up', registerView, name='sign_up'),
    path('sign_out', LogoutView.as_view(next_page='site-root'), name='sign_out'),
]
