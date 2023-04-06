from .models import *
from django.db.models import Count


menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        # {'title': 'Войти', 'url_name': 'login'}, 19урок 2.19 Регистрация
        ]


class DataMixin:  # урок 17 будет формировать нужный контекст по умолчанию
    paginate_by = 3  # 18 урок 17:00 перенесли из ArticleHome

    def get_user_context(self, **kwargs):
        context = kwargs  # формируем словарь из тех именнованых параметров которые переданы функции get_user_context
        cats = Category.objects.annotate(Count('article'))  # вместо нижней строки делаем чтобы не вывдить категорию,
        # которая не имеет ни одной записи
        # cats = Category.objects.all()  # будем формировать список категорий
        
        user_menu = menu.copy()  # 17 урок 19.10, если пользоваетль не авторизован 'Добавить статью' не показывать
        if not self.request.user.is_authenticated:
            user_menu.pop(1)  # удаляем из menu, которое тут наверху, второй элемент 'Добавить статью'
        context['menu'] = user_menu

        # context['menu'] = menu  # и добавляем в context(словарь) еще menu, которое тут в начале(вверху страницы)
        context['cats'] = cats  # формируется контекст для рубрик общий код для всех классов представлений
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
