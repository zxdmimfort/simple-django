from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    return HttpResponse("Страница приложения workers.")


def categories(request: HttpRequest):
    return HttpResponse("<h1>HAHAHA</h1>")
