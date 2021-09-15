from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from news.models import News
import re


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', help_text='Подсказка #1',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}))

    email = forms.EmailField(label='Почта',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title

# Несвязанная форма
# class NewsForm(forms.Form):
#     title = forms.CharField(max_length=150, label='Название новости',
#                             widget=forms.TextInput(
#                                 attrs={'class': 'form-control'}))
#     content = forms.CharField(label='Текс', required=False,
#                               widget=forms.Textarea(
#                                   attrs={
#                                       'class': 'form-control',
#                                       'rows': 5
#                                   }))
#     is_published = forms.BooleanField(label='Опубликовать', initial=True)
#     category = forms.ModelChoiceField(empty_label='Выберите категорию',
#                                       label='Категория',
#                                       queryset=Category.objects.all(),
#                                       widget=forms.Select(
#                                           attrs={'class': 'form-control'}))
