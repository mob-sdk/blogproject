#自定义的模板标签
"""
比如比较简单的 {% static %} 模板标签，这个标签帮助我们在模板中引入静态文件。
还有比较复杂的如 {% for %} {% endfor%} 标签。这里我们希望自己定义一个模板标签，
例如名为 show_recent_posts 的模板标签，它可以这样工作：我们只要在模板中写入 {% show_recent_posts %}，
那么模板中就会渲染一个最新文章列表页面，这和我们在编写博客首页面视图函数是类似的。
首页视图函数中从数据库获取文章列表并保存到 post_list 变量，然后把这个 post_list 变量传给模板，模板使用 for 模板标签循环这个文章列表变量，从而展示一篇篇文章。
这里唯一的不同是我们从数据库获取文章列表的操作不是在视图函数中进行，而是在模板中通过自定义的 {% show_recent_posts %} 模板标签进行。
"""

from django import template
from ..models import Post,Category,Tag
#这里我们首先导入 template 这个模块，然后实例化了一个 template.Library 类，

register = template.Library()
#并将函数 show_recent_posts 装饰为 register.inclusion_tag，这样就告诉 django，这个函数是我们自定义的一个类型为 inclusion_tag 的模板标签。
#inclusion_tag 装饰器的参数 takes_context 设置为 True 时将告诉 django，在渲染 _recent_posts.html 模板时，
#不仅传入show_recent_posts 返回的模板变量，同时会传入父模板（即使用 {% show_recent_posts %} 模板标签的模板）上下文
@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    #inclusion_tag 模板标签和视图函数的功能类似，它返回一个字典值，字典中的值将作为模板变量，传入由 inclusion_tag 装饰器第一个参数指定的模板。
    #当我们在模板中通过 {% show_recent_posts %}使用自己定义的模板标签时，django 会将指定模板的内容使用模板标签返回的模板变量渲染后替换。
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }

#归档模板标签
@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    #这里 Post.objects.dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间（已去重），
    # 且是 Python 的 date 对象，精确到月份，降序排列。接受的三个参数值表明了这些含义，一个是 created_time ，
    # 即 Post 的创建时间，month 是精度，order='DESC' 表明降序排列（即离当前越近的时间越排在前面）。
    # 例如我们写了 3 篇文章，分别发布于 2017 年 2 月 21 日、2017 年 3 月 25 日、2017 年 3 月 28 日，
    # 那么 dates 函数将返回 2017 年 3 月 和 2017 年 2 月这样一个时间列表，且降序排列，从而帮助我们实现按月归档的目的。
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }

#分类模板标签
@register.inclusion_tag('blog/inclusions/_categories.html',takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all(),
    }

#标签云模板标签
@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }