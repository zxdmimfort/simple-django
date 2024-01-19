from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm


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


class ProfileUser(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    model = get_user_model()
    form_class = ProfileUserForm
    extra_context = {"title": "Профиль пользователя"}

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("users:profile")
