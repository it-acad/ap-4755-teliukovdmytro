from django.contrib import admin
from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Відображення ID та імені автора у списку
    list_display = ('id', 'name', 'surname')  
    # Фільтр для швидкого пошуку
    list_filter = ('id', 'surname')# Register your models here.
