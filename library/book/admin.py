from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # 1. Додаткові поля у списку книг
    list_display = ('id', 'name', 'count', 'description') 
    
    # 2. Фільтри для швидкого пошуку за id, назвою книги та авторами
    # Примітка: переконайтеся, що у моделі Book поле зв'язку називається саме 'authors' або 'author'
    list_filter = ('id', 'name', 'authors') 

    # 3. Візуальний розподіл полів на блоки в картці редагування книги
    fieldsets = (
        ('Дані, що не змінюються', {
            'fields': ('name', 'authors'),
            'description': 'Основна незмінна інформація про видання.' # Опис блоку робиться так
        }),
        ('Дані, що змінюються', {
            'fields': ('count', 'description'), # 'count' та 'description' перенесено сюди
            'description': 'Динамічна інформація про наявність або видачу.'
        }),
    )