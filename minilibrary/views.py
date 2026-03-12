from django.shortcuts import render
from django.http import HttpResponseNotFound
from .models import Book
from django.db.models import Q

# Create your views here.


def index(request):
    try:
        books = Book.objects.all()
        query = request.GET.get("query_search")
        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__name__icontains=query) |
                Q(genres__name__icontains=query)
            ).distinct()

        return render(request, 'minilibrary/minilibrary.html', context={
            "text": "Welcome to the Mini Library!",
            "name": "Tito",
            "books": books,
            "query": query,
        })
    except Exception as e:
        return HttpResponseNotFound(f"Error fetching books: {e}")
