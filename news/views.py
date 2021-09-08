from django.http import HttpResponse
from django.shortcuts import render

from news.models import News, Category


def index(request):
    news = News.objects.all()
    return render(request, 'news/index.html',
                  {'news': news, 'title': 'Список новостей', })


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html',
                  {'news': news, 'category': category, })