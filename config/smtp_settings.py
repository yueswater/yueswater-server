import os

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465

EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "sungpinyue@gmail.com")

raw_password = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_HOST_PASSWORD = raw_password.replace(" ", "")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER