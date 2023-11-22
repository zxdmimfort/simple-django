from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template.defaulttags import url
from django.urls import reverse


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
]
data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
]


def index(request: HttpRequest):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
    }
    return render(request, 'workers/index.html', data)


def about(request: HttpRequest):
    data = {
        'title': 'О сайте',
    }
    return render(request, 'workers/about.html', data)


def add_page(request: HttpRequest):
    return HttpResponse("Добавление статьи")


def contact(request: HttpRequest):
    return HttpResponse("Обратная связь")


def login(request: HttpRequest):
    return HttpResponse("Авторизация")


def show_post(request, post_id):
    return HttpResponse(f"<h1>Отображение статьи с id = {post_id}</h1>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
