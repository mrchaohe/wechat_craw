from django.db import models

# Create your models here.
from account.models import Account

class Article(models.Model):
    # 文章链接表
    aid = models.CharField(max_length=32,primary_key=True,help_text="文章id,具有唯一标识")
    pid = models.ForeignKey(Account, on_delete=models.SET_NULL,null=True,help_text="公众号id")
    name = models.CharField(max_length=128,help_text="文章标题")
    link = models.CharField(max_length=256,help_text="文章链接")
    cover = models.CharField(max_length=256,help_text="封面链接")
    status = models.IntegerField( default=0,help_text="状态 0 未下载 1下载完成")
    create_time = models.DateField(auto_now=True,help_text="记录创建时间")
    update_time = models.DateField(auto_now=True,help_text="记录更新时间")

    class Meta:
        verbose_name = "article"


class TaskStatus(models.Model):
    # 下载任务状态表
    id = models.AutoField(primary_key=True,help_text="任务id")
    pid = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True,help_text="公众号id")
    start_time = models.DateField(help_text="任务开始时间")
    end_time = models.DateField(help_text="任务结束时间")
    keyword = models.CharField(max_length=32, default="",help_text="查询关键字")
    status = models.IntegerField(default=0,help_text="任务状态0 待运行 1运行中 2 运行完成")
    pagenum = models.IntegerField(default=0,help_text="上次运行页码")
    timegap = models.IntegerField(default=0,help_text="下载间隔时间")
    link_cnt = models.IntegerField(default=0,help_text="上次记录的文章链接数")
    down_cnt = models.IntegerField(default=0,help_text="上次下载的文章数")
    total = models.IntegerField(default=0,help_text="上次的文章总数")
    create_time = models.DateField(auto_now=True,help_text="任务创建时间")
    update_time = models.DateField(auto_now=True,help_text="任务修改时间")
    
    class Meta:
        verbose_name = "task_status"