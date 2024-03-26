from django.contrib import admin

# Register your models here.

from article.models import Article, TaskStatus
from article.urls import get_custom_urls



from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.utils.html import format_html


class TaskStatusAdmin(admin.ModelAdmin):
    fields = ("pid", "start_time", "end_time","timegap")
    list_display  = ("id", "pid","status", "start_time", "end_time","timegap","link_cnt", "down_cnt", "total", "create_time")

    def get_urls(self):
        return get_custom_urls(self) + super(TaskStatusAdmin, self).get_urls()
    
    def buttons(self, obj):
        button_html = """<a class="changelink" href="/admin/article/taskstatus/{}/action/">编辑</a>""".format(obj.id)
        return format_html(button_html)
    buttons.short_description = "执行"
    list_display  = ("id", "pid","status", "start_time", "end_time","timegap","link_cnt", "down_cnt", "total", "create_time", "buttons")


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("aid", "name", "pid", "link", "cover", "create_time", "update_time")

    def has_add_permission(self, request):
        return False

    # 重写 has_change_permission 方法以取消修改权限
    def has_change_permission(self, request, obj=None):
        return False
    
    


admin.site.register(Article, ArticleAdmin)
# TaskStatusAdmin.get_urls = get_custom_urls
admin.site.register(TaskStatus, TaskStatusAdmin)
