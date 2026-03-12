from django.shortcuts import render
from django.http import HttpResponseNotFound
from .models import Book
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
# Create your views here.


def index(request):
    try:
        books = Book.objects.all()
        query = request.GET.get("query_search")
        date_start = request.GET.get("start")
        date_end = request.GET.get("end")
        if date_end == "":
            date_end = timezone.now().date().strftime("%Y-%m-%d")

        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__name__icontains=query) |
                Q(genres__name__icontains=query)
            ).distinct()

        if date_start and date_end:
            books = books.filter(
                publication_date__range=[date_start, date_end]
            )
        elif date_end:
            books = books.filter(publication_date__lte=date_end)

        paginator = Paginator(books, 10)  # Show 10 books per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        query_params = request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        query_string = query_params.urlencode()

        return render(request, 'minilibrary/minilibrary.html', context={
            "text": "Welcome to the Mini Library!",
            "name": "Tito",
            "page_obj": page_obj,
            "query": query,
            "query_string": query_string,
        })
    except Exception as e:
        return HttpResponseNotFound(f"Error fetching books: {e}")
