from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from article.models import Article, TaskStatus

def action(request):
    """执行task"""
    return HttpResponse("12345")
    return JsonResponse({"hello": "world"})

