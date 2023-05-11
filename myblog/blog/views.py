# Представление/ контроллер/ вьюха
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.contrib.auth.decorators import login_required # 17 урок
from django.core.paginator import Paginator  # 18 урок
from django.views.generic import ListView, DetailView, CreateView  # 15 урок
# from django.contrib.auth.forms import UserCreationForm  # 19 урок Регистрация нужна если использовать встроенную форму, мы используем свою RegisterUserForm из forms.py поэтому можно удалить.
from django.contrib.auth.mixins import LoginRequiredMixin  # 17 урок 14.40 Для class, чтобы 'Добавление статьи'
# виден только зарегистрированый пользователь, для функций @login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView  # 20 урок
from django.contrib.auth.forms import AuthenticationForm  # 20 урок
from django.contrib.auth import logout, login  # 20 урок
from django.views.generic.edit import FormView  # 23 урок
from django.views import View  # я сам


from .models import *
from .forms import *
from .utils import *
# render - обрабатывает html шаблоны

# menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти'] было до 8 урока
'''menu = [{'title': 'О сайте', 'url_name': 'about'},  # 17 урок перенесли в utils.py формирование Mixins
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
        ]'''  


class ArticleHome(DataMixin, ListView):  # хорошо подошел class ListView тк хорошо создает список чеголибо
    model = Article  # атрибут model который будет ссылаться на модель Article связанный с этим списком Listview
    # атрибут model будет отображать список статей которые находятся в таблице Article
    # model = Article эта строчка выбирает все записи из таблицы и пытается их отобразить в виде списка
    # class ListView использует шаблин ИмяПриложения/ИмяМодели_list.html то есть у нас blog/Article_list.html
    template_name = 'blog/post_list.html'
    # template_name указывает какой шаблон использовать после того как закоментировали ниже def index(request)
    context_object_name = 'posts'  # т.к. класс представление ArticleHome формирует свою коллекцю object_list когда
    # когда загружает статьи из модели Article и posts в шаблоне html не получится использовать

    # extra_context = {'title': 'Главная страница'} так можно передать заголовок для страницы, но только для статических параметров
    # (не для списков) например menu = [{'title': 'О сайте', 'url_name': 'about'}, {'title': 'Добавить статью', 'url_name':.....} передать не получится
    # подойдет функция def get_context_data которая формирует и динамический и статический контекст
    # который передается потом в шаблон blog/post_list.html
    # paginate_by = 3   перенесли урок 18 17:00 в DataMixin

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # через super() обращаемся к базовому классу ListView
    # и с помощью get_context_data взять существующий контекст, и с помощью **kwargs распаковываем весь контекст
    # который уже сформирован (это 'posts'-список, 'title'-строка)
    # context это будет словарь
        c_def = self.get_user_context(title='Главная страница')  # словарь формируется на основе DataMixin который в utils.py
        # 17 урок убираем нижние три строки context и пишем верхнюю c_def
        '''context['menu'] = menu  # и добавляем в context(словарь) еще menu, которое в начале(вверху страницы)
        context['title'] = 'Главная страница'  # вместо статического extra_context = {'title': 'Главная страница'} в клссе ArticleHome
        context['cat_selected'] = 0  # отвечает за то что 'Все категории' подсвечивается как выбраная на Главной странице '''
        context = dict(list(context.items()) + list(c_def.items()))  # объединяем два словаря
        return context

    def get_queryset(self):  # выводить только те посты которые is_published
        return Article.objects.filter(is_published=True)


''' 15 урок вместо функции класс представления ListView
def index(request):  # request это ссылка на запрос HttpRequest с информацией о запросе, кукис и тд
    posts = Article.objects.all()
    # return render(request, 'blog/post_list.html', {'post': post, 'menu': menu, 'title': 'Главная страница'})
    # в return несколько словарей в 8 уроке заменили на context=context
    # cats = Category.objects.all()  после 11 урока добавили blog_tags.py
    context = {
        'posts': posts,
        # 'cats': cats,   после 11 урока добавили blog_tags.py
        'menu': menu,
        'title': 'Главная тсраница',
        'cat_selected': 0,
    }
    return render(request, 'blog/post_list.html', context=context)
'''

'''  проверить 
class About(DataMixin, View):
    def get(self, request):
        return render(request, 'blog/about.html', {'title': 'О сайте'})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # через super() обращаемся к базовому классу ListView
    # и с помощью get_context_data взять существующий контекст, и с помощью **kwargs распаковываем весь контекст
    # который уже сформирован (это 'posts'-список, 'title'-строка)
    # context это будет словарь
        c_def = self.get_user_context(title='О сайте')
        # 17 урок убираем нижние две строки context и пишем верхнюю c_def
        # context['title'] = 'Добавление статьи' 
        # context['menu'] = menu  # и добавляем в context(словарь) еще menu, которое в начале(вверху страницы)
        context = dict(list(context.items()) + list(c_def.items()))  # объединяем два словаря
        return context
'''

def about(request):  # Paginator для функции. Он встроен в класс ListView, но т.к. 
    # у нас тут функция то строк будет больше: 
    contact_list = Article.objects.all()  # 18 урок. Сначала считаем список всех статей.
    paginator = Paginator(contact_list, 3)  # 18 урок. Самостоятельно создаем экземпляр класса Paginator.
    page_number = request.GET.get('page')  # 18 урок. Получаем номер текущей страницы из GET запроса, из него
    # берем параметр 'page'
    page_obj = paginator.get_page(page_number)  # 18 урок. Формируем объект page_obj который
    # будет содержать список элементов текущей страницы. Обращаемся к paginator и с помощью
    # get_page указываем странцу которую получили из GET. Затем в return page_obj добавили
    return render(request, 'blog/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'Про сайт'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm  # атрибут form_class указывает на
    # класс формы AddPostForm, который будет связан с классом представления AddPage, т.к.
    # т.к. CreateView работает с формами то нужно указать класс фомры AddPostForm 
    template_name = 'blog/addpage.html'
    success_url = reverse_lazy('home') # можно добавить чтобы после добавления статьи перенаправлять
    # на главную страницу, иначе через models.py и def get_absolute_url(self) переходит на созданную страницу
    login_url = reverse_lazy('home')  # если пользователь не авторизован то перенаправляется на Главную

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # через super() обращаемся к базовому классу ListView
    # и с помощью get_context_data взять существующий контекст, и с помощью **kwargs распаковываем весь контекст
    # который уже сформирован (это 'posts'-список, 'title'-строка)
    # context это будет словарь
        c_def = self.get_user_context(title='Добавление статьи')
        # 17 урок убираем нижние две строки context и пишем верхнюю c_def
        # context['title'] = 'Добавление статьи' 
        # context['menu'] = menu  # и добавляем в context(словарь) еще menu, которое в начале(вверху страницы)
        context = dict(list(context.items()) + list(c_def.items()))  # объединяем два словаря
        return context

'''  # 15 урок поменяли на class AddPage(CreateView)
@login_required  # 17 урок, страница видна для зарегистрированных пользователей
def addpage(request):
    if request.method == 'POST':  # нажата кнопка ВВОД/ВХОД пришел POST (request='POST')
        form = AddPostForm(request.POST, request.FILES)  # AddPostForm сформирует форму на основе POST (где хранятся заполненые данные)
        # request.FILES - передает список файлов которые были переданы на сервер из формы
        if form.is_valid():  # если проверка не пройдена то форма вернется ЗАПОЛНЕНОЙ
            # print(form.cleaned_data)  # если пройдет то очищается
            # try:
            form.save()  # т.к. form связана с моделью Article (см. forms.py class Meta, model = Article )
            # это поменяли в 14 уроке вместо то что снизу
            # Article.objects.create(**form.cleaned_data) в 14 уроке убрали, 
            # а в 13 уроке тут сохраняли данные, распкаковывая словарь (**form.cleaned_data)
            # и передавали методу create чтобы создать новую запись.
            return redirect('home')
            # except: (14 урок)убрали, т.к. form.save() сам делает все проверки и показывает ошибки ввода форм
            #    form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()  # первый переход выдает пустую форму
    return render(request, 'blog/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})
'''


# def contact(request):
#    return HttpResponse('Обратная связь')


class ContactFormView(DataMixin, FormView):  # 23 урок FormView стандартный класс для форм которые не привязаны к модели, у
    # нас форма Обратной Связи не будет работать с БД.
    form_class = ContactForm  # наш шаблон из forms.py
    template_name = 'blog/contact.html'
    success_url = reverse_lazy('home')  # перенап-е пользователя при успешной заполнении формы

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # через super() обращаемся к базовому классу ListView
    # и с помощью get_context_data взять существующий контекст, и с помощью **kwargs распаковываем весь контекст
    # который уже сформирован (это 'posts'-список, 'title'-строка)
    # context это будет словарь
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):  # 23 урок вызывается при успешном заполнении всех полей формы Обратной Связи
        print(form.cleaned_data)  # выводит в Терминал данные полученые из формы
        return redirect('home')


# def login(request):  с 20 урока
#    return HttpResponse('Авторизация')


def pageNotFond(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(DataMixin, DetailView):  # 15 урок заменили функцию def ShowPost()
    model = Article
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'  # DetailView ищет в urls.py по пути path('post/<slug:slug>/' а не path('post/<slug:post_slug>/'
    # поэтому прописываем вручную. Если ипользуется не slug а id тогда pk_url_kwarg = 'pk' или 'post_pk'
    context_object_name = 'post'  # выше в ArticleHome(ListView) описано

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # через super() обращаемся к базовому классу ListView
    # и с помощью get_context_data взять существующий контекст, и с помощью **kwargs распаковываем весь контекст
    # который уже сформирован (это 'posts'-список, 'title'-строка)
    # context это будет словарь
        c_def = self.get_user_context(title=context['post'])
        # 17 урок убираем нижние две строки context и пишем верхнюю c_def
        # context['title'] = context['post']
        # context['menu'] = menu  # и добавляем в context(словарь) еще menu, которое в начале(вверху страницы)
        context = dict(list(context.items()) + list(c_def.items()))
        return context


'''  15 урок заменили на class ShowPost
def show_post(request, post_slug):  # 12 урок, был post_id стал post_slug
    post = get_object_or_404(Article, slug=post_slug)  # 12 урок, было (Article, pk=post_id)
    # 12урок, было return HttpResponse(f'Отображение статьи с id = {post_id}')

    context = {  # 12 урок
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,  # шаблон знает какую рубрику сделать выбраной, а остальные дулает ссылками (актеры-выбран (подсвечен), спорт и певцы-активные ссылки)
    }
    return render(request, 'blog/post.html', context=context)
'''


class ArticleCategory(DataMixin, ListView):
    model = Article
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'  # выше в ArticleHome(ListView) описано
    allow_empty = False  # при вводе несуществующей категории /actery3445/ будет
    # выдавать ошибку 404, а не какую-то другую
    paginate_by = 2

    def get_queryset(self):  # выводить только те посты которые is_published
        return Article.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)
        # cat__slug обращаемся к полю slug таблицы cat связаной с текущей записью

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # через super() обращаемся к базовому классу ListView
    # и с помощью get_context_data взять существующий контекст, и с помощью **kwargs распаковываем весь контекст
    # который уже сформирован (это 'posts'-список, 'title'-строка)
    # context это будет словарь
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat), cat_selected=context['posts'][0].cat_id)
        # 17 урок убираем нижние три строки context и пишем верхнюю c_def
        # context['menu'] = menu  # и добавляем в context(словарь) еще menu, которое в начале(вверху страницы)
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)  # вместо статического extra_context = {'title': 'Категория - певцы'} в классе ArticleHome, берем первую запись [0] из context['posts'] и обращаемся к атрибуту cat - он представляет
        # собой объект который представялет из себя название категории и появляется название вверху страницы 'Категория- певцы'.
        # context['cat_selected'] = context['posts'][0].cat_id  # отвечает за то что выбраная категория'Певцы', '...' будет
        # подсвечивается как выбраная на Главной странице
        context = dict(list(context.items()) + list(c_def.items()))
        return context


def houston(request):
    return render(request, 'blog/houston.html')


'''
def show_category(request, cat_slug):  # cat_id):  # САМ ЗАМЕНИЛ
    cat = Category.objects.get(slug=cat_slug)  # небыло строки
    posts = Article.objects.filter(cat_id=cat.id)  # выбирает все посты с cat_id = 1 Певицы
    # cats = Category.objects.all()   после 11 урока добавили blog_tags.py

    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        # 'cats': cats,  после 11 урока добавили blog_tags.py
        'menu': menu,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat.id,  # cat.id та которую прочитали из запроса (request, cat_id)
    }
    return render(request, 'blog/post_list.html', context=context)
'''


class RegisterUser(DataMixin, CreateView):  # 19 урок
    # form_class = UserCreationForm  - стандартная форма Django служит для регистрации пользователей, но т.к. мы сделали в forms.py свою форму RegisterUserForm то form_class будет с нашей формой ниже написано.
    form_class = RegisterUserForm 
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')  # перенаправление пользоваетля при успешной авторизации

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # через super() обращаемся к базовому классу ListView
    # и с помощью get_context_data взять существующий контекст, и с помощью **kwargs распаковываем весь контекст
    # который уже сформирован (это 'posts'-список, 'title'-строка)
    # context это будет словарь
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):  # 20 урок вызывается при успешной проверке формы регистрации
        user = form.save()  # самостоятельно сохраняем форму в БД (те добавляем пользователя в БД)
        login(self.request, user)  # login функция авторизовывает пользователя
        return redirect('home')


class LoginUser(DataMixin, LoginView):  # 20 урок, LoginView для авторизации пользователя
    form_class = LoginUserForm  # AuthenticationForm стандартная форма для авторизации, но
    # т.к. у нас своя LoginUserForm в forms.py то указываем ее.
    template_name = 'blog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # через super() обращаемся к базовому классу ListView
    # и с помощью get_context_data взять существующий контекст, и с помощью **kwargs распаковываем весь контекст
    # который уже сформирован (это 'posts'-список, 'title'-строка)
    # context это будет словарь
        c_def = self.get_user_context(title='Авторизаця')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):  # 20 урок, 5.20 вместо этой функции можно прописать LOGIN_REGIRECT_URL = '/'  в settings под MEDIA_URL - 
        return reverse_lazy('home')


def logout_user(request):  # 20 урок
    logout(request)  # logout стандартная функция Django
    return redirect('login')
