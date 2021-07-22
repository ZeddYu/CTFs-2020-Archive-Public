from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from .settings import LOGIN_REDIRECT_URL

urlpatterns = [
    path('', RedirectView.as_view(url=LOGIN_REDIRECT_URL), name='site-root'),
    # path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('posts/', include('posts.urls', namespace='posts')),
]
