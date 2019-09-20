import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.shortcuts import render
from .models import Post,Category
from django.shortcuts import get_object_or_404
import markdown
# Create your views here.
from django.http import HttpResponse
#编写首页视图，web服务器的作用是接收来自用户的HTTP请求，根据请求内容作出相应的处理，并把处理的结果包装成HTTP响应返回给用户
def index(request):
    #使用模型管理器object，并使用all()方法从数据库里获取了全部的文章，存在post_list变量里，all()方法返回一个queryset（列表的数据结构）
    #博文文章列表是按照文章发表的时间倒序排列的，最新的文章在最前面，所以我们紧接着调用了order_by方法对这个返回的queryset进行排序。排序依据的字段是create_time
    #排序依据的字段是create_time，文章创建的时间，-意思是逆序，不加-则是正序
    post_list = Post.objects.all().order_by('-created_time')
    #先接收了一个request参数，这个request是django封装好的HTTP请求，它是类HTTPrequest的一个实例
    #然后我们直接返回一个HTTP响应给用户，HTTP响应也是django封装好的，是HTTPresponse的一个实例，只是给我们传了一个自定义的字符串参数

    #render参数根据我们传入的参数来构造httpresponse，我们首先把http请求传了进去，然后render根据第二个参数的值 blog/index.html 找到这个模板
    #并读取模板中的内容，之后render根据我们传入的context参数的值把模板中的变量替换成我们传递的变量的值，
    #{{ title }}被替换成了context字典中的title对应的值
    #最终，我们的HTML模板中的内容字符串被传递给HTTPResponse对象并返回给浏览器（django在render函数里隐式的帮我们完成这个过程）
    return render(request,'blog/index.html',context={
     'post_list': post_list
    })

def detail(request,pk):
    # URL 捕获的文章 id（也就是 pk，这里 pk 和 id 是等价的）获取数据库中文章 id 为该值的记录，然后传递给模板
    post = get_object_or_404(Post,pk=pk)
    #get_object_or_404 方法，其作用就是当传入的 pk 对应的 Post 在数据库存在时，
    #就返回对应的 post，如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在。

    #没有直接用 markdown.markdown() 方法来渲染 post.body 中的内容
    #先实例化了一个 markdown.Markdown 对象 md，和 markdown.markdown() 方法一样，也传入了 extensions 参数
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        #'markdown.extensions.toc',
        TocExtension(slugify=slugify),
    ])
    """
    文章内容的标题被设置了锚点，点击目录中的某个标题，页面就会跳到该文章内容中标题所在的位置，这时候浏览器的 URL 显示的值可能不太美观，比如像下面的样子：
    http://127.0.0.1:8000/posts/8/#_1

    http://127.0.0.1:8000/posts/8/#_3
    #_1 就是锚点，Markdown 在设置锚点时利用的是标题的值，由于通常我们的标题都是中文，Markdown 没法处理，
    所以它就忽略的标题的值，而是简单地在后面加了个 _1 这样的锚点值。为了解决这一个问题，需要修改一下传给 extentions 的参数
    和之前不同的是，extensions 中的 toc 拓展不再是字符串 markdown.extensions.toc ，而是 TocExtension 的实例。TocExtension 在实例化时其 slugify 参数可以接受一个函数，
    这个函数将被用于处理标题的锚点值。Markdown 内置的处理方法不能处理中文标题，所以我们使用了 django.utils.text 中的 slugify 方法，该方法可以很好地处理中文。
    """
    """
           这样我们在模板中显示  post.body  的时候，就不再是原始的 Markdown 文本了，
           而是解析过后的 HTML 文本。注意这里我们给 markdown 解析函数传递了额外的参数 extensions，它是对 Markdown 语法的拓展，这里使用了三个拓展，
           分别是 extra、codehilite、toc。extra 本身包含很多基础拓展，而 codehilite 是语法高亮拓展，
           这为后面的实现代码高亮功能提供基础，而 toc 则允许自动生成目录。
    """
    """
    类似于一堆乱码一样的 HTML 标签，这些标签本应该在浏览器显示它自身的格式，但是 django 出于安全方面的考虑，
    任何的 HTML 代码在 django 的模板中都会被转义（即显示原始的 HTML 代码，而不是经浏览器渲染后的格式）。
    为了解除转义，只需在模板变量后使用 safe 过滤器即可，告诉 django，这段文本是安全的，
    你什么也不用做。在模板中找到展示博客文章内容的 {{ post.body }} 部分，为其加上 safe 过滤器：{{ post.body|safe }}，大功告成，这下看到预期效果了。
    """
    """
    接着我们便使用该实例的 convert 方法将 post.body 中的 Markdown 文本解析成 HTML 文本。而一旦调用该方法后，实例 md 就会多出一个 toc 属性，这个属性的值就是内容的目录，
    我们把 md.toc 的值赋给 post.toc 属性（要注意这个 post 实例本身是没有 toc 属性的，我们给它动态添加了 toc 属性，这就是 Python 动态语言的好处）。
    """
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc,re.S)
    """
    正则表达式去匹配生成的目录中包裹在 ul 标签中的内容，如果不为空，说明目录，
    就把 ul 标签中的值提取出来（目的是只要包含目录内容的最核心部分，多余的 HTML 标签结构丢掉）赋值给 post.toc；
    否则，将 post 的 toc 置为空字符串，然后我们就可以在模板中通过判断 post.toc 是否为空，来决定是否显示侧栏目录
    """
    post.toc = m.group(1) if m is not None else ''


    return render(request,'blog/detail.html',context={
        'post': post
    })

def archive(request,year,month):
    #Python 中调用属性的方式通常是 created_time.year，但是由于这里作为方法的参数列表，所以 django 要求我们把点替换成了两个下划线，即 created_time__year
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

#分类页面
def category(request, pk):
    #这里我们首先根据传入的 pk 值（也就是被访问的分类的 id 值）从数据库中获取到这个分类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html',context={'post_list':post_list})