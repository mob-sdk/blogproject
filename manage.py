#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

#在运行的时候，django会接收一个--setting-model的参数，用于指定执行命令
def main():
    #if 参数没有指定，则会会从DJANGO_SETTINGS_MODULE---环境变量中获取值，当删除了blogproject.settings后
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogproject.settings')
    #如果把blogproject.settings 的值改为 blogproject.settings.local，运行开发服务器的时候django会加载 blogproject/settings/loacl.py
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
