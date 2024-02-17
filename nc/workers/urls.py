from django.urls import path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path("", views.WorkerHome.as_view(), name="home"),
    path("about/", views.about, name="about"),
    path("addpage/", views.AddPage.as_view(), name="add_page"),
    path("login/", views.login, name="login"),
    path("post/<slug:post_slug>/", views.ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", views.WorkerCategory.as_view(), name="category"),
    path("tag/<slug:tag_slug>/", views.WorkerTag.as_view(), name="tag"),
    path("edit/<slug:post_slug>/", views.UpdatePage.as_view(), name="edit"),
    path("delete/<slug:post_slug>/", views.DeletePage.as_view(), name="delete"),
    path("contact/", views.ContactFormView.as_view(), name="contact"),
]
