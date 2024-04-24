from .base import *

DEBUG = False
ALLOWED_HOSTS = ["scvready.online", "www.scvready.online"]


STATIC_ROOT = BASE_DIR / "static/"

CSRF_TRUSTED_ORIGINS = ["https://scvready.online"]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
