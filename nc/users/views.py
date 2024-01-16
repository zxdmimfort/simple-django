from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView

from users.forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}


class LogoutUser(LogoutView):
    pass


def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return render(request, "users/register_done.html")
    else:
        form = RegisterUserForm()
    return render(request, "users/register.html", {"form": form})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/register.html"
    extra_context = {"title": "Регистрация"}
    success_url = "users:login"
