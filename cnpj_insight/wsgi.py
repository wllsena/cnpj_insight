"""
WSGI config for cnpj_insight project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cnpj_insight.settings")
application = get_wsgi_application()


# def main() -> None:
#     """
#     Initialize Django WSGI application.

#     Sets the default Django settings module and retrieves the WSGI application.
#     """
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cnpj_insight.settings")
#     application = get_wsgi_application()

#     return application


# if __name__ == "__main__":
#     application = main()

    
