from django.contrib.auth import get_user_model


User = get_user_model()
if not(User.objects.filter(username="root")):
    user = User.objects.create_superuser("root", "root@root.root", "root")

