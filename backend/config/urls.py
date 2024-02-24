from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.decorators.cache import cache_page

from config.settings import settings
from workers.sitemaps import PostSitemap, CategorySitemap
from workers.views import page_not_found, server_error, permission_denied

sitemaps = {
    "posts": PostSitemap,
    "cats": CategorySitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("workers.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("users/", include("users.urls", namespace="users")),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("captcha/", include("captcha.urls")),
    path(
        "sitemap.xml",
        cache_page(86400)(sitemap),
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
handler500 = server_error
handler403 = permission_denied

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Работники"
