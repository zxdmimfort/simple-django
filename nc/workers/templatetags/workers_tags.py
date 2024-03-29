from django import template
import workers.views as views
from workers.models import Category, TagPost
from workers.utils import menu

register = template.Library()


@register.simple_tag()
def get_menu():
    return menu


@register.inclusion_tag("workers/list_categories.html")
def show_categories(cat_selected_id=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected_id}


@register.inclusion_tag("workers/list_tags.html")
def show_all_tags():
    return {"tags": TagPost.objects.all()}
