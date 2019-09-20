from django.urls import path

from . import views

app_name = 'blog'
urlpatterns=[
    #绑定的写法是把网址和对应的处理函数作为参数传给path函数（第一个参数是网址，第二个参数是处理函数）
    #另外传递一个name参数，作为处理函数index的别名
    path('',views.index, name='index'),
    #我们通过 app_name='blog' 告诉 django 这个 urls.py 模块是属于 blog 应用的，这种技术叫做视图函数命名空间。
    #我们看到 blog\urls.py 目前有两个视图函数，并且通过 name 属性给这些视图函数取了个别名，分别是 index、detail
    path('posts/<int:pk>/',views.detail,name='detail'),
    path('archives/<int:year>/<int:month>',views.archive,name='archive'),
    path('categories/<int:pk>/', views.category, name='category'),
]
"""
    django 会用这个规则去匹配用户实际输入的网址，如果匹配成功，就会调用其后面的视图函数做相应的处理。
    比如说我们本地开发服务器的域名是 http://127.0.0.1:8000，
    那么当用户输入网址 http://127.0.0.1:8000 后，
    django 首先会把协议 http、域名 127.0.0.1 和端口号 8000 去掉，此时只剩下一个空字符串，
    而 '' 的模式正是匹配一个空字符串，
    于是二者匹配，django 便会调用其对应的 views.index 函数。
"""

"""
首页视图匹配的 URL 去掉域名后其实就是一个空的字符串。对文章详情视图而言，每篇文章对应着不同的 URL。
比如我们可以把文章详情页面对应的视图设计成这个样子：当用户访问 <网站域名>/posts/1/ 时，显示的是第一篇文章的内容，
而当用户访问 <网站域名>/posts/2/ 时，显示的是第二篇文章的内容，这里数字代表了第几篇文章，也就是数据库中 Post 记录的 id 值。
以 posts/ 开头，后跟一个整数，并且以 / 符号结尾，如 posts/1/、 posts/255/ 等都是符合规则的
<int:pk> 是 django 路由匹配规则的特殊写法，其作用是从用户访问的 URL 里把匹配到的数字捕获并作为关键字参数传给其对应的视图函数 detail
detail(request, pk=255)
 int 整数类型，还有 str 字符类型、uuid
"""