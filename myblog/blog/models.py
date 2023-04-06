from django.db import models
from django.urls import reverse
# MODELS тут прописываем ВСЕ модели для ВЗАИМОДЕЙСТВИЯ с БД
# {% url %} лучше использовать когда используется не элемент базы данных
# Создать функцию {{ p.get_absolute_url }} и использовать когда достается из базы данных


class Article(models.Model):
    # видео 9, 11.54
    # все атрибуты ниже (внутри Модели) определяют набор и тип полей в таблице БД
    # и не содержит конкретных данных, а Джанго через Миграции формирует струтуру таблицы
    # а в SHELL через w1=... присваиваем данные 
    # w1 = Article(title='t1') в БД title = t1 (str)
    # cat = models.ForeignKey('Category'....) в БД cat = Category()
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')  # 12 урок
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото') # отсортирует фото в папки по дате
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категорияяя')
    # в переменной cat 'Category' передано как строка, иначе будет ошибка т.к. класс Article выше, чем Category 
    # можно передать и не строку Category, но тогда Класс Category надо переносить выше

    def __str__(self):  # выводит в режиме SHELL при обращении к objects.title имя title(категории), а не Article object (1)
        return self.title

    def get_absolute_url(self):  # функция так же добавляет кнопку в админке -ПОСМОТРЕТЬ на САЙТЕ
        # А еще при добавлении поста в AddPage этой функцией перенаправляется на только что добавленную(созданную) страницу
        # return reverse('post', kwargs={'post_id': self.pk})  с 8 урока, 'post_id'подставится в шаблон в urls.py  path('post/<int:post_id>/'...
        return reverse('post', kwargs={'post_slug': self.slug})  # 12 урок, был post_id стал post_slug

    class Meta:  # класс используется админ панелью для настройки/отображения класса Article
        verbose_name = 'Famous people'
        verbose_name_plural = 'Famous people'
        # ordering = ['time_create', 'title'] 18 урок 25:00 отключили сортировку для пагинации
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')  # 12 урок
    #  slug после 12 урока

    def __str__(self):  # выводит в режиме SHELL при обращении к objects.title имя title(категории), а не Article object (1)
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})  # {'cat_id': self.pk}) # САМ ЗАМЕНИЛ

    class Meta:  # класс используется админ панелью для настройки/отображения класса Article
        verbose_name = 'Категория'
        verbose_name_plural = 'Categoryyy'
        ordering = ['id']
