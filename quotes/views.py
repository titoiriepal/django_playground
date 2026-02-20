from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.


def days_weeks(request, day):
    phrases = {
        "monday": "Monday is the start of the week.",
        "tuesday": "Tuesday is the second day of the week.",
        "wednesday": "Wednesday is the middle of the week.",
        "thursday": "Thursday is the fourth day of the week.",
        "friday": "Friday is the last day of the workweek.",
        "saturday": "Saturday is a day for relaxation and fun.",
        "sunday": "Sunday is a day for rest and family time."
    }

    day = day.lower()

    quote_text = phrases.get(day, "No quote available for this day.")

    return HttpResponse(f"{quote_text}")
