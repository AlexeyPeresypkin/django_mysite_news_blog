from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', test, name='test'),
    path('rubric/<int:pk>', get_rubrick, name='rubric'),
]
