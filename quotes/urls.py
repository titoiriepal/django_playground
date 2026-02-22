from django.urls import path
from . import views

urlpatterns = [
    path("<int:day>", views.days_weeks_with_numbers,
         name="day-quotes-with-numbers"),
    path("<str:day>", views.days_weeks, name="day-quotes"),
]
