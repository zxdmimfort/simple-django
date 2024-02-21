from django.contrib.sitemaps import Sitemap

from workers.models import Worker, Category


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Worker.published.all()

    def lastmod(self, obj):
        return obj.time_update


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Category.objects.all()
