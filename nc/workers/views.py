from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    return HttpResponse("Страница приложения workers.")


def categories(request: HttpRequest, cat_id: int):
    return HttpResponse(f"<h1>Categories:</h1><p>id: {cat_id}")


def categories_by_slug(request: HttpRequest, cat_slug):
    return HttpResponse(f"<h1>Categories by slug:</h1><p>id: {cat_slug}</p>")


def archive(request: HttpRequest, year):
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")
