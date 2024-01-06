import uuid
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView

from workers.forms import AddPostForm, UploadFileForm
from workers.models import Worker, Category, TagPost, UploadFiles

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


def show_post(request, post_slug):
    post = get_object_or_404(Worker, slug=post_slug)

    data = {
        "title": post.title,
        "menu": menu,
        "post": post,
        "cat_selected": 1,
    }

    return render(request, "workers/post.html", context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class WomenCategory(ListView):
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


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.workers.filter(is_published=Worker.Status.PUBLISHED).select_related(
        "cat"
    )

    data = {
        "title": f"Тег: {tag.tag}",
        "menu": menu,
        "posts": posts,
        "cat_selected": None,
    }

    return render(request, "workers/index.html", data)
