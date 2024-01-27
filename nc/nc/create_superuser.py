from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

User = get_user_model()
if not(User.objects.filter(username="root")):
    user = User.objects.create_superuser("root", "root@root.root", "root")
if not(Group.objects.filter(name="social")):
    content_type = ContentType.objects.get_for_model(User)
    permission = Permission.objects.create(codename="social_auth", name="Social Auth", content_type=content_type)
    group = Group.objects.create(name="social")
    group.permissions.add(permission)
