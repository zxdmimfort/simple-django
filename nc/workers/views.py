import uuid
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect

from workers.forms import AddPostForm, UploadFileForm
from workers.models import Worker, Category, TagPost, UploadFiles

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


def index(request: HttpRequest):
    posts = Worker.published.all().select_related("cat")

    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": posts,
        "cat_selected": 0,
    }
    return render(request, "workers/index.html", data)


# def handle_uploaded_file(f):
#     name = f.name
#     import os
#     from uuid import uuid4
#
#     ext = os.path.splitext(name)[1]
#     name = str(uuid4()) + ext
#
#     with open(f"uploads/{name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#     return name


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


def add_page(request: HttpRequest):
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = AddPostForm()
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


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Worker.published.filter(cat_id=category.pk).select_related("cat")

    data = {
        "title": f"Рубрика : {category.name}",
        "menu": menu,
        "posts": posts,
        "cat_selected": category.pk,
    }

    return render(request, "workers/index.html", data)


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
