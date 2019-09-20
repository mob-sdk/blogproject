from django.contrib import admin
from .models import Post,Category,Tag
# Register your models here.
#文章列表页面，我们只看到了文章的标题，但是我们希望它显示更加详细的信息，这需要我们来定制 admin

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','modified_time','category','author']
    """
    化新增文章时，填写表单数据的不合理的地方。文章的创建时间和修改时间应该根据当前时间自动生成，
    而现在是由人工填写，还有就是文章的作者应该自动填充为后台管理员用户，那么这些自动填充数据的字段就不需要在新增文章的表单中出现了。
    """
    fields = ['title','body','excerpt','category','author'] #fields 中定义的字段就是表单中展现的字段



    """
    填充创建时间，修改时间和文章作者的值
    """
    """
    而如果用户登录了我们的站点，那么 django 就会将这个用户实例绑定到 request.user 属性上，
    我们可以通过 request.user 取到当前请求用户，然后将其关联到新创建的文章即可。
    
    它有一个 save_model 方法，这个方法只有一行代码：obj.save()。
    它的作用就是将此 Modeladmin 关联注册的 model 实例（这里 Modeladmin 关联注册的是 Post）保存到数据库。
    这个方法接收四个参数，其中前两个，一个是 request，即此次的 HTTP 请求对象，第二个是 obj，即此次创建的关联对象的实例，
    于是通过复写此方法，就可以将 request.user 关联到创建的 Post 实例上，然后将 Post 数据再保存到数据库
    """
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request,obj,form,change)


# 把新增的 Postadmin 也注册进来
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)