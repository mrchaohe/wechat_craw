# 此处采用django admin 作为前端，在admin 文件中使用

from django.urls import path

from article.views import action

def get_custom_urls(admin_class):
    return [
        path('/admin/article/taskstatus/action/', admin_class.admin_site.admin_view(action), name='custom_action'),
    ]