from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404


def new_users_handler(backend, user, response, *args, **kwargs):
    try:
        group = Group.objects.get(name="social")
        user.groups.add(group)
    except Group.DoesNotExist as e:
        print(f"Failed add social user to social group. Error {e}")
