"""
WSGI config for blogproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogproject.settings')
#application 是 在线上环境时 Gunicorn 加载运行的，将这里面的 DJANGO_SETTINGS_MODULE 改为 blogproject.settings.production
application = get_wsgi_application()
