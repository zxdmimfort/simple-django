from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from workers.models import Worker, Category, TagPost


class MarriedFilter(admin.SimpleListFilter):
    title = "Статус работника"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ("married", "Замужем"),
            ("single", "Не замужем"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "married":
            return queryset.filter(husband__isnull=False)
        elif self.value() == "single":
            return queryset.filter(husband__isnull=True)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "post_photo", "time_create", "is_published", "cat")
    list_display_links = ("title",)
    list_editable = ("is_published", "cat")
    list_per_page = 5
    ordering = ["time_create", "title"]
    actions = ["set_published", "set_draft"]
    search_fields = ["title__startswith", "cat__name"]
    list_filter = [MarriedFilter, "cat__name", "is_published"]
    fields = [
        "title",
        "slug",
        "content",
        "post_photo",
        "photo",
        "cat",
        "husband",
        "tags",
    ]
    filter_horizontal = ["tags"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["post_photo"]
    save_on_top = True

    @admin.display(description="Изображение")
    def post_photo(self, worker: Worker):
        if worker.photo:
            return mark_safe(f"<img src='{worker.photo.url}' width='50'>")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Worker.Status.PUBLISHED)
        self.message_user(request, f"{count} записи(ей) опубликованы!")

    @admin.action(description="Скрыть выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Worker.Status.DRAFT)
        self.message_user(
            request, f"{count} записи(ей) сняты с публикации!", messages.WARNING
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ["name", "slug"]
    # readonly_fields = ['slug']
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("id", "name")
    list_display_links = ("id", "name")

@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    fields = ["tag", "slug"]
    prepopulated_fields = {"slug": ("tag",)}
    list_display = ("id", "tag")
    list_display_links = ("id", "tag")
