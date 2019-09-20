#存放线上环境的配置
#在使用 manage.py 执行命令时，加载的是 local.py 的设置，而使用 gunicorn 运行项目时，使用的是 production.py 的设置。
from .common import *
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY'] #从环境变量中获取

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['hellodjango-blog-tutorial.zmrenwu.com']