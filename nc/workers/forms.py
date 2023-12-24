from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from workers.models import Category, Husband


@deconstructible
class RussianValidator:
    """
    Кастомный валидатор. Явно прикрепляется к полю в коллекцию validators.
    """

    ALLOWED_CHARS = (
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- "
    )
    code = "russian"

    def __init__(self, message=None):
        self.message = (
            message
            if message
            else "Должны присутствовать только русские символы, дефис и пробел."
        )

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        min_length=5,
        label="Заголовок",
        widget=forms.TextInput(attrs={"class": "form-input"}),
        validators=[
            # RussianValidator(),
            # MinLengthValidator(5, message="Минимум 5 символов"),
            # MaxLengthValidator(255, message="Максимум 255 символов"),
        ],
        error_messages={
            "min_length": "Слишком короткий заголовок",
            "required": "Заголовок обязателен",
        },
    )
    slug = forms.SlugField(
        max_length=255,
        label="URL slug",
        validators=[
            MinLengthValidator(5, message="Минимум 5 символов"),
            MaxLengthValidator(100, message="Максимум 100 символов"),
        ],
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"cols": 50, "rows": 5}),
        required=False,
        label="Контент",
    )
    is_published = forms.BooleanField(required=False, label="Статус")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории")
    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(), required=False, label="Муж"
    )

    def clean_title(self):
        """
        Вызывается при проверке формы методом is_valid
        clean_<название поля формы>
        """
        title = self.cleaned_data["title"]
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- "

        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError(
                "Должны присутствовать только русские символы, дефис и пробел."
            )
