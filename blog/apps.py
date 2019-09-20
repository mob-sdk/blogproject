from django.apps import AppConfig

"""
admin 首页每个版块代表一个 app，比如 BLOG 版块表示 blog 应用，版块标题默认显示的就是应用名。
应用版块下包含了该应用全部已经注册到 admin 后台的 model，之前我们注册了 Post、Category 和 Tag，所以显示的是这三个 model，显示的名字就是 model 的名字
BLOG 版块的标题 BLOG，一个版块代表一个应用，显然这个标题使用应用名转换而来，
有一个 BlogConfig 类，其继承自 AppConfig 类，看名字就知道这是和应用配置有关的类
"""
class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = '博客' #可以修改app在admin后台的显示的名字
