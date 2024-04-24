from django.contrib.auth import get_user_model
from django.db import models

from workers.models import Worker

User = get_user_model()


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="comments"
    )
    post = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=300, verbose_name="Текст комментария")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
