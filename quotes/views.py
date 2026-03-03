from django.shortcuts import render
from django.http import (
    # HttpResponseNotFound,
    HttpResponseRedirect,
    # Http404
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
        "quotes/index.html",
        context={
            "title": "Quotes for Days of the Week",
            "days": days,
        }
    )


def days_weeks(request, day):

    try:
        phrase = phrases[day.lower()]
    except KeyError:
        # raise Http404()  # This will render the default 404 page if DEBUG in
        # playground settings is False
        return render(
            request,
            '404.html',
            context={
                "title": "Page not found",
            }
        )

    return render(
        request,
        "quotes/daily_phrase.html",
        context={
            "title": f"Quote for {day.capitalize()}",
            "day": day.capitalize(),
            "phrase": phrase,
        }
    )

    # return HttpResponse(f"{phrases.get(
    #     day.lower(),
    #     "No quote available for this day.",
    # )}")


def days_weeks_with_numbers(request, day):

    if day < 1 or day > len(days):
        return render(
            request,
            '404.html',
            context={
                "title": "Page not found",
            }
        )

    redirect_path = reverse("day-quotes", args=[days[day - 1]])

    return HttpResponseRedirect(redirect_path)
