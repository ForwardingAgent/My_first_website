from django import template
from blog.models import *

register = template.Library()  # создаем экземпляр класса Librery()
# через который происходит регистрация собственных шаблонных тегов


# здесть с помощью ПРОСТОГО(simple_tag) тэга мы возвращали коллекцию Category.objects.all(), а не html страницу
@register.simple_tag(name='getcats')  # за счет этого @ функция превращается в тэг
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


# ВКЛЮЧАЮЩИЙ(inclusion_tag) тэг позволяет формировать свой собственный шаблон и возвращать фрагмент html страницы
@register.inclusion_tag('blog/list_categories.html')  # за счет этого @ функция превращается в 
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    
    return {'cats': cats, 'cat_selected': cat_selected}
