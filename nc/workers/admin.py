from django.contrib import admin, messages

from workers.models import Worker, Category


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    list_editable = ('is_published', 'cat')
    list_per_page = 5
    ordering = ['time_create', 'title']
    actions = ['set_published', 'set_draft']

    @admin.display(description="Краткое описание", ordering='content')
    def brief_info(self, worker: Worker):
        return f"Описание {len(worker.content)} символов."

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Worker.Status.PUBLISHED)
        self.message_user(request, f"{count} записи(ей) опубликованы!")

    @admin.action(description="Скрыть выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Worker.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
