from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect

from workers.forms import AddPostForm
from workers.models import Worker, Category, TagPost

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},
]


def index(request: HttpRequest):
    posts = Worker.published.all().select_related('cat')

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'workers/index.html', data)


def about(request: HttpRequest):
    data = {
        'title': 'О сайте',
        'menu': menu,
    }
    return render(request, 'workers/about.html', data)


def add_page(request: HttpRequest):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            try:
                Worker.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()
    return render(request, 'workers/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})


def contact(request: HttpRequest):
    return HttpResponse("Обратная связь")


def login(request: HttpRequest):
    return HttpResponse("Авторизация")


def show_post(request, post_slug):
    post = get_object_or_404(Worker, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'workers/post.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Worker.published.filter(cat_id=category.pk).select_related('cat')

    data = {
        'title': f'Рубрика : {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }

    return render(request, 'workers/index.html', data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.workers.filter(is_published=Worker.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'workers/index.html', data)
