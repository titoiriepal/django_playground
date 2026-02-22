# from django.shortcuts import render
from django.http import (
    HttpResponse,
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

    list_items = ""
    for day in days:
        day_url = reverse("day-quotes", args=[day])
        list_items += f'<li><a href="{day_url}">{day.capitalize()}</a></li>'
    html_content = f"""
    <h1>Quotes for Days of the Week</h1>
    <ul>
        {list_items}
    </ul>
    """
    return HttpResponse(html_content)


def days_weeks(request, day):

    return HttpResponse(f"{phrases.get(
        day.lower(),
        "No quote available for this day.",
    )}")


def days_weeks_with_numbers(request, day):

    if day < 1 or day > len(days):
        return HttpResponseNotFound("<h2>Invalid day number.</h2>")

    redirect_path = reverse("day-quotes", args=[days[day - 1]])

    return HttpResponseRedirect(redirect_path)
