from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.shortcuts import render


def index(request: HttpRequest):
    return HttpResponse("Страница приложения workers.")


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
        raise Http404()
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
