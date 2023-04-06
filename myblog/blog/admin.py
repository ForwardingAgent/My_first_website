from django.contrib import admin
from .models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')  # добавляет id слева строки Article
    list_display_links = ('id', 'title')  # делает слово Article актвным для проваливания и редактирования
    search_fields = ('title', 'content')  # добавляет поиск
    list_editable = ('is_published',)  # в админке можно ставить и снимать галки Публикация
    list_filter = ('is_published', 'time_create')  # добавляет поля по которым можно фильтровать список статей
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
