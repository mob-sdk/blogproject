"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

# 利用include函数把blog应用下的urls.py文件包含进来，''是一个空字符串，django会吧这个字符串和后面的include的urls.py文件中的url拼接
# 如果把''改成'blog/'，而在blog/urls中写的url是''，是空字符串。那么django最终匹配的就是blog/ 加上一个空字符串，即 'blog/'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blog.urls')),
    path('',include('comments.urls')),
    path('',include('users.urls'))

]
