from django.shortcuts import render
# from django.http import HttpResponse
from datetime import date
# Create your views here.


def home(request):
    return render(
        request,
        "landing/landing.html",
        context={
            "name": "tito",
            "age": 30,
            "today": date.today(),
            "stack": ["Python", "Django", "JavaScript", "PHP", "React"],

        },
    )
