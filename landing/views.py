from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
# Create your views here.


def home(request):
    return render(
        request,
        "landing/landing.html",
        context={
            "title": "Landing Page",
            "name": "tito",
            "age": 30,
            "today": date.today(),
            "stack": [
                {'id': 1, 'name': "Python"},
                {'id': 2, 'name': "Django"},
                {'id': 3, 'name': "JavaScript"},
                {'id': 4, 'name': "PHP"},
                {'id': 5, 'name': "React"},
            ],

        },
    )


def stack(request, tool):
    return HttpResponse(
        f"Here you can find all the information about {tool} in my stack"
    )
