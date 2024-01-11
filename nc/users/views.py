from django.http import HttpResponse
from django.shortcuts import render


def login_user(request):
    return HttpResponse("login")


def logout_user(request):
    return HttpResponse("logout")
