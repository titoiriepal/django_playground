from django.shortcuts import render
from django.http import (
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.urls import reverse

# Create your views here.

phrases = {
    "monday": "Monday is the start of the week.",
    "tuesday": "Tuesday is the second day of the week.",
    "wednesday": "Wednesday is the middle of the week.",
    "thursday": "Thursday is the fourth day of the week.",
    "friday": "Friday is the last day of the workweek.",
    "saturday": "Saturday is a day for relaxation and fun.",
    "sunday": "Sunday is a day for rest and family time."
}

days = list(phrases.keys())


def index(request):

    return render(
        request,
        "quotes/quotes.html",
        context={
            "title": "Quotes for Days of the Week",
            "days": days,
        }
    )


def days_weeks(request, day):

    return render(
        request,
        "quotes/daily_phrase.html",
        context={
            "title": f"Quote for {day.capitalize()}",
            "day": day.capitalize(),
            "phrase": phrases.get(
                day.lower(),
                "No quote available for this day.",
            ),
        }
    )

    # return HttpResponse(f"{phrases.get(
    #     day.lower(),
    #     "No quote available for this day.",
    # )}")


def days_weeks_with_numbers(request, day):

    if day < 1 or day > len(days):
        return HttpResponseNotFound("<h2>Invalid day number.</h2>")

    redirect_path = reverse("day-quotes", args=[days[day - 1]])

    return HttpResponseRedirect(redirect_path)
