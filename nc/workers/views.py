from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)

from workers.forms import AddPostForm, UploadFileForm, ContactForm
from workers.models import Worker, TagPost, UploadFiles, Category


class DataMixin:
    title_page = None
    paginate_by = 3
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context["title"] = self.title_page

    def get_mixin_context(self, context: dict, **kwargs: dict) -> dict:
        if self.title_page:
            context["title"] = self.title_page

        context["cat_selected"] = None
        context.update(kwargs)
        return context


class WorkerHome(DataMixin, ListView):
    template_name = "workers/index.html"
    context_object_name = "posts"
    title_page = "Главная страница"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            super().get_context_data(**kwargs),
            cat_selected=0,
            page=self.request.GET.get("page"),
        )

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


@login_required
def about(request: HttpRequest):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data["file"])
            fp.save()
    else:
        form = UploadFileForm()

    from workers.utils import menu

    return render(
        request, "workers/about.html", {"title": "О сайте", "menu": menu, "form": form}
    )


class AddPage(PermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "workers/addpage.html"
    success_url = reverse_lazy("home")
    title_page = "Добавление статьи"
    permission_required = "workers.add_worker"  # <application>.<action>_<table>

    # form_valid нужен только в FormView. В CreateView он уже реализован
    # Или для добавления автора
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


def login(request: HttpRequest):
    return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    # model = Worker
    template_name = "workers/post.html"
    # Задаем параметр пути как в urls
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=context["post"].title,
            edit_url=reverse_lazy(
                "edit", kwargs={"post_slug": self.kwargs["post_slug"]}
            ),
        )

    # Для DetailView используем get_object вместо get_queryset
    def get_object(self, object_list=None):
        return get_object_or_404(
            Worker.published, slug=self.kwargs[self.slug_url_kwarg]
        )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class WorkerCategory(DataMixin, ListView):
    template_name = "workers/index.html"
    context_object_name = "posts"
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # cat = context["posts"][0].cat
        cat = get_object_or_404(Category.objects, slug=self.kwargs["cat_slug"])
        return self.get_mixin_context(
            context,
            title="Категория - " + cat.name,
            cat_selected=cat.id,
        )

    def get_queryset(self):
        return Worker.published.filter(
            cat__slug=self.kwargs["cat_slug"]
        ).select_related("cat")


class WorkerTag(DataMixin, ListView):
    template_name = "workers/index.html"
    context_object_name = "posts"
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        return self.get_mixin_context(context, title="Тег: " + tag.tag)

    def get_queryset(self, *, object_list=None, **kwargs):
        return Worker.published.filter(
            tags__slug=self.kwargs["tag_slug"]
        ).select_related("cat")


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Worker
    form_class = AddPostForm
    template_name = "workers/addpage.html"
    slug_url_kwarg = "post_slug"
    success_url = reverse_lazy("home")
    title_page = "Редактирование статьи"
    permission_required = "workers.change_worker"


class DeletePage(LoginRequiredMixin, DeleteView):
    model = Worker
    success_url = reverse_lazy("home")
    slug_url_kwarg = "post_slug"
    title_page = "Удаление статьи"


class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = "workers/contact.html"
    success_url = reverse_lazy("home")
    title_page = "Обратная связь"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
