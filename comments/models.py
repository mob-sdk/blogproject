from django.db import models
from django.utils import timezone
# Create your models here.

class Comment(models.Model):
    name = models.CharField('姓名',max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址',blank=True)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间',default=timezone.now)
    post = models.ForeignKey('blog.Post',verbose_name='文章',on_delete=models.CASCADE)

    class Meta:
        # 通过 verbose_name 来指定对应的 model 在 admin 后台的显示名称，
        # 这里 verbose_name_plural 用来表示多篇文章时的复数显示形式。 在中文中是一样的，英文不同
        verbose_name='评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}:{}'.format(self.name, self.text[:20])