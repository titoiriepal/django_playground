from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the quotes index.")


def monday(request):
    return HttpResponse("Hi, it's Monday!")


def tuesday(request):
    return HttpResponse("Hi, it's Tuesday!")


def wednesday(request):
    return HttpResponse("Hi, it's Wednesday!")


def thursday(request):
    return HttpResponse("Hi, it's Thursday!")


def friday(request):
    return HttpResponse("Hi, it's Friday!")


def saturday(request):
    return HttpResponse("Hi, it's Saturday!")


def sunday(request):
    return HttpResponse("Hi, it's Sunday!")
