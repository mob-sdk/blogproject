from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
import markdown
# Create your models here.
#Category是标准的python类，它继承了model.Model类，类名是Category，它有一个属性 name，是models.CharField(max_length=100)的实例
from django.utils.html import strip_tags


class Category(models.Model):
    #django会在数据库里创建一个Category的表，表里有name 的列名，和id列
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
#标签类
class Tag(models.Model):
    """
    标签Tag简单，和Category一样
    继承model.Model
    """
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
#文章类
class Post(models.Model):
    #标题
    title = models.CharField('标题',max_length=70)
    #正文
    body = models.TextField('正文')

    #文章的创建时间和最后一次修改的时间，存储时间的字段用 DatatimeField类型
    """
    这里 default 既可以指定为一个常量值，也可以指定为一个可调用（callable）对象，我们指定 timezone.now 函数，
    这样如果没有指定 created_time 的值，django 就会将其指定为 timezone.now 函数调用后的值。timezone.now 是 django 提供的工具函数，返回当前时间。
    因为 timezone 模块中的函数会自动帮我们处理时区，所以我们使用的是 django 为我们提供的 timezone 模块，而不是 Python 提供的 datetime 模块来处理时间。
    """
    created_time = models.DateTimeField('创建日期',default=timezone.now())
    modified_time = models.DateTimeField('修改日期',default=timezone.now())



    #文章的摘要，默认情况下charfield要求我们必须存入数据，否则报错
    #指定charfield的blank=true参数值后就可以允许空值了
    excerpt = models.CharField('摘要',max_length=200, blank=True)

    #分类与标签，分类和标签的模型都已经在上面定义了
    #我们这里吧文章对应的数据库表和分类，标签对应的数据库关联起来，但是关联形式不同
    #我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是foreignkey，即一对多的关联关系
    #django2.0以后，foreignkey必须传入一个on_delete 参数用来指定 当关联的数据被删除时，被关联的数据的行为，我们这里假定
    #当某个分类被删除时，该分类下全部的文章也同时被删除，因此使用ManyToManyField，表示多对多关系
    category = models.ForeignKey(Category,verbose_name='分类', on_delete=models.CASCADE)#models.CASCADE 级联删除
    tags = models.ManyToManyField(Tag,verbose_name='标签',blank=True)

    #文章的作者，这里的user是从django.contrib.models 导入的
    #django.contrib.models是django内置应用，专门用于处理网站用户的注册，登录的流程，user是django为我们已经写好的用户模型
    #我们通过foreignkey把文章和user关联起来，因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关系
    #和category类似
    author = models.ForeignKey(User, verbose_name='作者',on_delete=models.CASCADE)
    #通过 model 的内部类 Meta 中来定义

    """
    给每个 Field 都传入了一个位置参数，参数值即为 field 应该显示的名字（如果不传，django 自动根据 field 名生成）。
    这个参数的名字也叫 verbose_name，绝大部分 field 这个参数都位于第一个位置，
    但由于 ForeignKey、ManyToManyField 第一个参数必须传入其关联的 Model，所以 category、tags 这些字段我们使用了关键字参数 verbose_name。
    """

    class Meta:
        #通过 verbose_name 来指定对应的 model 在 admin 后台的显示名称，
        #这里 verbose_name_plural 用来表示多篇文章时的复数显示形式。 在中文中是一样的，英文不同
        verbose_name='文章'
        verbose_name_plural=verbose_name
        #django 允许我们在 models.Model 的子类里定义一个名为 Meta 的内部类，通过这个内部类指定一些属性的值来规定这个模型类该有的一些特性，
        #例如在这里我们要指定 Post 的排序方式。首先看到 Post 的代码，在 Post 模型的内部定义的 Meta 类中，指定排序属性 ordering
        ordering = ['-created_time']
        #ordering 属性用来指定文章排序方式，['-created_time'] 指定了依据哪个属性的值进行排序，这里指定为按照文章发布时间排序，且负号表示逆序排列。
        #列表中可以有多个项，比如 ordering = ['-created_time', 'title'] 表示首先依据 created_time 排序，如果 created_time 相同，则再依据 title 排序
        #这样指定以后所有返回的文章列表都会自动按照 Meta 中指定的顺序排序，因此可以删掉视图函数中对文章列表中返回结果进行排序的代码

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)

    """
    例如一些第三方应用中也可能有叫 index、detail 的视图函数，那么怎么把它们区分开来，防止冲突呢？
    方法就是通过 app_name 来指定命名空间，命名空间具体如何使用将在下面介绍。
    如果你忘了在 blog/urls.py 中添加这一句，接下来你可能会得到一个 NoMatchReversed 异常。
    为了方便地生成上述的 URL，我们在 Post 类里定义一个 get_absolute_url 方法，注意 Post 本身是一个 Python 类，在类中我们是可以定义任何方法的。
    """
    #自定义 get_absolute_url 方法
    #记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
        #由于 get_absolute_url 这个方法（我们定义在 Post 类中的）返回的是 post 对应的 URL

    """
            注意到 URL 配置中的 path('posts/<int:pk>/', views.detail, name='detail') ，
            我们设定的 name='detail' 在这里派上了用场。看到这个 reverse 函数，它的第一个参数的值是 'blog:detail'，
            意思是 blog 应用下的 name=detail 的函数，由于我们在上面通过 app_name = 'blog' 告诉了 django 这个 URL 模块是属于 blog 应用的，
            因此 django 能够顺利地找到 blog 应用下 name 为 detail 的视图函数，于是 reverse 函数会去解析这个视图函数对应的 URL，
            我们这里 detail 对应的规则就是 posts/<int:pk>/ int 部分会被后面传入的参数 pk 替换，所以，如果 Post 的 id（或者 pk，这里 pk 和 id 是等价的） 是 255 的话，
            那么 get_absolute_url 函数返回的就是 /posts/255/ ，这样 Post 自己就生成了自己的 URL。
    """