from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView

from workers.forms import AddPostForm, UploadFileForm
from workers.models import Worker, TagPost, UploadFiles

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


class WorkerHome(ListView):
    template_name = "workers/index.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cat_selected"] = int(self.request.GET.get("cat_id", 0))
        context["title"] = "Главная страница"
        context["menu"] = menu
        return context

    def get_queryset(self):
        if cat_id := int(self.request.GET.get("cat_id", 0)):
            return Worker.published.filter(cat_id=cat_id).select_related("cat")
        return Worker.published.all().select_related("cat")


def create_name_file(name: str):
    import os
    from uuid import uuid4

    ext = os.path.splitext(name)[1]
    name = str(uuid4()) + ext
    return name


def about(request: HttpRequest):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data["file"])
            fp.save()
    else:
        form = UploadFileForm()

    return render(
        request, "workers/about.html", {"title": "О сайте", "menu": menu, "form": form}
    )


class AddPage(View):
    def get(self, request: HttpRequest):
        form = AddPostForm()
        return render(
            request,
            "workers/addpage.html",
            {"menu": menu, "title": "Добавление статьи", "form": form},
        )

    def post(self, request: HttpRequest):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")

        return render(
            request,
            "workers/addpage.html",
            {"menu": menu, "title": "Добавление статьи", "form": form},
        )


def contact(request: HttpRequest):
    return HttpResponse("Обратная связь")


def login(request: HttpRequest):
    return HttpResponse("Авторизация")


class ShowPost(DetailView):
    # model = Worker
    template_name = "workers/post.html"
    # Задаем параметр пути как в urls
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["post"].title
        context["menu"] = menu
        return context

    # Для DetailView используем get_object вместо get_queryset
    def get_object(self, object_list=None):
        return get_object_or_404(Worker.published, slug=self.kwargs[self.slug_url_kwarg])


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class WorkerCategory(ListView):
    template_name = "workers/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat
        context["title"] = "Категория - " + cat.name
        context["menu"] = menu
        context["cat_selected"] = cat.id
        return context

    def get_queryset(self):
        return Worker.published.filter(
            cat__slug=self.kwargs["cat_slug"]
        ).select_related("cat")


class WorkerTag(ListView):
    template_name = "workers/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        context["title"] = "Тег: " + tag.tag
        context["menu"] = menu
        context["cat_selected"] = None
        return context

    def get_queryset(self, *, object_list=None, **kwargs):
        return Worker.published.filter(tags__slug=self.kwargs["tag_slug"]).select_related("cat")
