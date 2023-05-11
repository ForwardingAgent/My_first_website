from django.urls import path, re_path
from blog.views import *

urlpatterns = [
    # path('', index, name='home') c 15 урока
    path('', ArticleHome.as_view(), name='home'),
    # path('about/', About.as_view(), name='about'),  # сам сделал
    path('about/', about, name='about'),  # http://127.0.0.1:8000/about/
    # до 8 урока было 2 пути

    path('addpage/', AddPage.as_view(), name='add_page'),  # 15 урок 25.25
    # path('addpage/', addpage, name='add_page'),   # http://127.0.0.1:8000/addpage/

    path('contact/', ContactFormView.as_view(), name='contact'),  # 23 урок
    # path('contact/', contact, name='contact'),  # http://127.0.0.1:8000/contact/

    path('login/', LoginUser.as_view(), name='login'),  # 20 урок
    # path('login/', login, name='login'),  # http://127.0.0.1:8000/login/

    path('logout/', logout_user, name='logout'),  # 20 урок

    path('register/', RegisterUser.as_view(), name='register'),  # 19 урок http://127.0.0.1:8000/register/ 

    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),  # 15 урок 21.00
    # path('post/<slug:post_slug>/', show_post, name='post'),  # 12 урок, отображение в адрес cтроке страницы по slug
    # отображение в адрес cтроке номер страницы по slug, http://127.0.0.1:8000/post/silvestr-stallone/
    # path('post/<int:post_id>/', show_post, name='post'), 
    # верхний path - отображение в адрес cтроке номер страницы по id, http://127.0.0.1:8000/post/1


    path('category/<slug:cat_slug>/', ArticleCategory.as_view(), name='category'),  # c 15 урока 15:37
    # path('category/<slug:cat_slug>/', show_category, name='category'),  # 12 урок
    # отображение в адрес cтроке номер страницы по slug, http://127.0.0.1:8000/category/aktery/
    # path('category/<int:cat_id>/', show_category, name='category'),
    # верхний path - отображение в адрес cтроке катеогри по id, http://127.0.0.1:8000/category/1

    path('houston/', houston, name='Houston'),
] 
