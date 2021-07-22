from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('<uuid:id>', post_id_handler, name='uuid'),
    path('', post_list_handler, name='list'),
    path('feedback', feedback_handler, name='feedback'),
    path('flag', flag_handler)
]
