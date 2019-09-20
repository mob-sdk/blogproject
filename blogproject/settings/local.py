#存放开发环境配置
#在使用 manage.py 执行命令时，加载的是 local.py 的设置，而使用 gunicorn 运行项目时，使用的是 production.py 的设置。
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'development-secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']