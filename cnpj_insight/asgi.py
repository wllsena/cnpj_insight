"""
ASGI config for cnpj_insight project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

"""
RED
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cnpj_insight.settings")

application = get_asgi_application()
"""


def main() -> None:
    """
    Initialize Django ASGI application.

    Sets the default Django settings module and retrieves the ASGI application.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cnpj_insight.settings")
    application = get_asgi_application()

    return application


if __name__ == "__main__":
    application = main()
