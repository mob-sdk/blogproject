#表单
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        #在表单的内部类 Meta 里指定一些和表单相关的东西。model = Comment 表明这个表单对应的数据库模型是 Comment 类。
        # fields = ['name', 'email', 'url', 'text'] 指定了表单需要显示的字段，这里我们指定了 name、email、url、text 需要显示。
        fields = ['name', 'email', 'url', 'text']