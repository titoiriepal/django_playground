from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from .models import Book
from .forms import ReviewForm

# Create your views here.

User = get_user_model()


class Hello(View):
    def get(self, request):
        return HttpResponse("Hello, World! From CBV.")


class WelcomeView(TemplateView):
    template_name = 'minilibrary/welcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_books'] = Book.objects.count()
        return context


class BookListView(ListView):
    model = Book
    template_name = 'minilibrary/book_list.html'
    context_object_name = 'books'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_obj = context['page_obj']
        paginator = context['paginator']

        start = max(page_obj.number - 2, 1)
        end = min(page_obj.number + 2, paginator.num_pages)

        context['custom_page_range'] = range(start, end + 1)

        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'minilibrary/book_detail.html'
    context_object_name = 'book'
    # slug_field = 'id'
    # slug_url_kwarg = 'pk'


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


def add_review(request, book_id):
    # Lógica para agregar una reseña a un libro específico
    book = get_object_or_404(Book, id=book_id)
    form = ReviewForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            would_recommend = form.cleaned_data.get('would_recommend')
            if would_recommend:
                messages.success(
                    request, "Thank you for recommending this book!")

            messages.success(request, "Review added successfully!")
            # Redirige a la página principal después de agregar la reseña
            return redirect('recommend_book', book_id=book.id)
        else:
            messages.error(
                request,
                (
                    "There was an error with your review. "
                    "Please check the form and try again."
                ),
                extra_tags='danger'
            )

    return render(request, 'minilibrary/add_review.html',
                  context={
                      "form": form,
                      "book": book,
                  })
