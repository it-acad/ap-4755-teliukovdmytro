from django.urls import path
from . import views

urlpatterns = [
    # Головна сторінка авторів (порожній шлях всередині додатку)
    path('', views.author_list, name='author_list'),
]
