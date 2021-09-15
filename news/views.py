from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from news.forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from news.models import News, Category
from news.utils import MyMixin


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('news:home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('news:home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('news:login')


def test(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'],
                             form.cleaned_data['content'],
                             'send_from@yandex.ru',
                             ['send_to@yandex.ru'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('news:test')
            else:
                messages.error('Ошибка отправки')
        else:
            messages.error(request, 'Не заполнены поля')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    mixin_prop = 'Hello world'
    paginate_by = 2

    # queryset = News.objects.select_related('category')
    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related(
            'category')


# def index(request):
#     news = News.objects.all()
#     return render(request, 'news/index.html',
#                   {'news': news, 'title': 'Список новостей', })

class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'],
                                   is_published=True
                                   ).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsByCategory, self).get_context_data(**kwargs)
        context['title'] = self.get_upper(
            Category.objects.get(pk=self.kwargs['category_id']))
        return context


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html',
#                   {'news': news, 'category': category, })


class ViewNews(DetailView):
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'
    # pk_url_kwarg = 'news_id'


# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # login_url = '/admin/'
    # login_url = reverse_lazy('news:home')
    raise_exception = True
    # success_url = reverse_lazy('news:home')

#
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
