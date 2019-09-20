from django.shortcuts import render
from .form import RegisterForm
# Create your views here.
def register(request):
    #从get或者 post 请求中获取next 参数值
    #get请求中，next通过url传递， 即 /?next=value
    #post请求中，next通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    #首先尝试从用户的 GET 或者 POST 请求中获取 next 参数值，即在注册成功后需要跳转的 URL，如果有值，注册成功后跳转到该 URL，否则跳转回首页。

    #只有当请求为post时，才表示用户提交了注册请求
    if request.method == 'POST':
        #request.post是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        # 用这些注册的数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        #验证数据的合法性
        if form.is_valid():
            #如果数据合法，则保存到数据库中
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                #注册成功，跳转到首页
                return redirect('/')
    else:
        #请求如果不是POST，则表示用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    #渲染模板
    #如果用户正在访问注册页面，则渲染一个空的注册表单
    #如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    #同是不要忘记将该值传给模板，以维持 next 参数在整个注册流程中的传递。
    return render(request,'users/register.html',context={'form':form,'next':redirect_to})