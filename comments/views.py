
# Create your views here.
from django.contrib import messages
from blog.models import Post
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .form import CommentForm

#首先视图函数被 require_POST 装饰器装饰，从装饰器的名字就可以看出，
# 其作用是限制这个视图只能通过 POST 请求触发，因为创建评论需要用户通过表单提交的数据，而提交表单通常都是限定为 POST 请求，这样更加安全。
@require_POST
def comment(request, post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # 这里我们使用了 django 提供的一个快捷函数 get_object_or_404，
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(Post, pk=post_pk)

    # django 将用户提交的数据封装在 request.POST 中，这是一个类字典对象。
    # 我们利用这些数据构造了 CommentForm 的实例，这样就生成了一个绑定了用户提交数据的表单。
    form = CommentForm(request.POST)

    # 当调用 form.is_valid() 方法时，django 自动帮我们检查表单的数据是否符合格式要求。
    if form.is_valid():
        # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
        # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
        comment = form.save(commit=False)

        # 将评论和被评论的文章关联起来。
        comment.post = post

        # 最终将评论数据保存进数据库，调用模型实例的 save 方法
        comment.save()
        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')


        # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
        # 然后重定向到 get_absolute_url 方法返回的 URL。
        #另外我们使用了 redirect 快捷函数。这个函数位于 django.shortcuts 模块中，
        # 它的作用是对 HTTP 请求进行重定向（即用户访问的是某个 URL，但由于某些原因，服务器会将用户重定向到另外的 URL）。
        # redirect 既可以接收一个 URL 作为参数，也可以接收一个模型的实例作为参数（例如这里的 post）。
        # 如果接收一个模型的实例，那么这个实例必须实现了 get_absolute_url 方法，这样 redirect 会根据 get_absolute_url 方法返回的 URL 值进行重定向。
        return redirect(post)

    # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
    # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址。
    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')

    #否则说明用户提交的表单包含错误，我们将渲染一个 preview.html 页面，来展示表单中的错误，以便用户修改后重新提交。preview.html
    #使用 show_comment_form 模板标签来展示一个表单，然而不同的是，
    #这里我们传入由视图函数 comment 传来的绑定了用户提交的数据的表单实例 form，而不是渲染一个空表单。
    #因为视图函数 comment 中的表单实例是绑定了用户提交的评论数据，以及对数据进行过合法性校验的表单，因此当 django 渲染这个表单时，会连带渲染用户已经填写的表单数据以及数据不合法的错误提示信息，而不是一个空的表单了。
    return render(request, 'comments/preview.html', context=context)