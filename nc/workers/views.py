from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]
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


def categories(request: HttpRequest, cat_id: int):
    return HttpResponse(f"<h1>Categories:</h1><p>id: {cat_id}")


def categories_by_slug(request: HttpRequest, cat_slug):
    if request.GET:
        print(request.GET)
    elif request.POST:
        print(request.POST)
    return HttpResponse(f"<h1>Categories by slug:</h1><p>slug: {cat_slug}</p>")


def archive(request: HttpRequest, year):
    if year > 2023:
        uri = reverse('cats', args=('sport',))
        return HttpResponseRedirect(uri)

    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
