from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.forms import UserCreationForm  # 
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm  # 20 урок
from captcha.fields import CaptchaField  # 23 урок


# код 13 урока в самом внизу, как начинался FORMS.PY.
# AddPostForm(придумали сами) наследовался от (....Form)
# Cначала дублировали поля из models.py class Article в forms.py,
# чтобы показать способ использование форм, которые НЕ СВЯЗАННЫМИ ПОЛЯМИ.
# урок 14 показывает связь форм которые СВЯЗАННЫ (имеют одинаковые) ПОЛЯ.
# и тут AddPostForm наследуется от (.....ModelForm)


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # урок 14 3.50, добавили конструктор - def __init__(...), 
        # чтобы добавить в выпадающее меню в cat не ---, а 'Категория не выбрана'.
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Article  # model делает связь forms.py c Article
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        # fields -какие поля надо отобразить в форме
        # __all__ -показывать все поля кроме тех что заполняются автоматичеси
        # но лучше вместо __all__ прописывать вручную в [...].
        widgets = {  # widgets - задаем параметры формы - для title через class; - для content через coil': 60, 'rows'
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'coil': 60, 'rows': 10})
        }

    # СДЕЛАЛИ СОБСТВЕННЫЙ ВАЛИДАТОР 14 урок 11.10, 
    # проверка на валидность. Должно начинаться с clean_ + имя того что проверяем (title)
    # через коллекцию cleaned_data которая доступна в экземпляре класса AddPostForm
    # и по ключу ['title] получаем значение (title=...) которое ввел пользователь
    def clean_title(self):
        title = self.cleaned_data['title']  # в этой строке получаем данные по title
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return title

''' 14 урок заменили на класс выше
class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}))
        # forms.CharField - поле для ввода данных; 
        #  widget - означает что для ПОЛЯ ВВОДА применен класс form-input (видоизменяет форму ввода, длинее URL)
    slug = forms.SlugField(max_length=255, label='URL')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    is_published = forms.BooleanField(label='Публикация', required=False, initial=True)  
        # forms.BooleanField - формирует чекбокс опубликовано/не опубликовано; required - не обязательно к заполнению;
        # initial - делает чекбокс по умочанию отмеченым
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', empty_label='Категория не выбрана')
        # ModelChoiceField - показывает выпадающий список на основе всех Category.objects.all
'''


class RegisterUserForm(UserCreationForm):  # RegisterUserForm придумываем сами
    class Meta:  # расширяем стандартный класс UserCreationForm
        model = User  # это модель работающая с auth_user в базе данных
        fields = ('username', 'email', 'password1', 'password2')  # обязательно указать поля которые будут отображаться
        widgets = {  # оформление для каждого из этих полей, узнать о полях можно 19 урок 8.00
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }


class LoginUserForm(AuthenticationForm):  # 20 урок
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    # два поля формируются с помощью CharField, а widget - как отображать поля в браузере, одно
    # будет как поле ввода второе как поля для пароля (****) и далее через class стили этих форм


class ContactForm(forms.Form):  # 23 урок
    username = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(label='Я - человек')
