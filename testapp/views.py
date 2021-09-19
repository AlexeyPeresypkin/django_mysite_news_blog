from django.shortcuts import render

from testapp.models import Rubric


def test(request):
    return render(request, "testapp/testapp.html",
                  {'rubrics': Rubric.objects.all()})


def get_rubrick(request):
    pass
