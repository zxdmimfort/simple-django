import socket  # only if you haven't already imported this
from .base import *


DEBUG = True

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1"]

# MEDIA_ROOT = BASE_DIR / "media/"

AUTHENTICATION_BACKENDS += [
    "social_core.backends.vk.VKOAuth2",
    "social_core.backends.github.GithubOAuth2",
]
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_GITHUB_KEY = os.getenv("GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = os.getenv("GITHUB_SECRET")
SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv("VK_KEY")
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv("VK_SECRET")
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ["email"]
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
# SOCIAL_AUTH_REQUIRE_POST = True
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "users.pipeline.new_users_handler",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)
