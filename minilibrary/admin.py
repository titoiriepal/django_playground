from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Author, Genre, Book, BookDetail
from .models import Review, Recommendation, Loan

# Register your models here.

User = get_user_model()

admin.site.site_header = "Mini Library Admin"
admin.site.site_title = "Mini Library Admin Portal"
admin.site.index_title = "Welcome to the Mini Library Admin Portal"


@admin.action(description="Mark selected loans as returned")
def mark_as_returned(modeladmin, request, queryset):
    queryset.update(is_returned=True)


@admin.action(description="Mark selected loans as not returned")
def mark_as_not_returned(modeladmin, request, queryset):
    queryset.update(is_returned=False)


class LoanInLine(admin.TabularInline):
    model = Loan
    extra = 1


class ReviewInLine(admin.TabularInline):
    model = Review
    extra = 1


class BookDetailInLine(admin.StackedInline):
    model = BookDetail
    extra = 0
    verbose_name = "Book's Detail"


class CustomUserAdmin(BaseUserAdmin):
    inlines = [LoanInLine]
    list_display = ('username', 'email', 'is_staff', 'is_active')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('pages',)
    inlines = [ReviewInLine, BookDetailInLine]
    list_display = ('title', 'author', 'publication_date', 'pages')
    search_fields = ('title', 'author__name')
    list_filter = ('author', 'publication_date', 'genres')
    ordering = ['-publication_date']
    date_hierarchy = 'publication_date'
    autocomplete_fields = ('author', 'genres')

    fieldsets = (
        ("Information", {
            'fields': ('title', 'author', 'publication_date',)
        }),
        ("Additional Info", {
            'fields': ('pages', 'isbn', 'genres'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permisiion(self, request, obj=None):
        return request.user.is_staff


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)
    ordering = ['-birth_date']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]
    ordering = ['name']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ('loan_date',)
    list_display = ('user', 'book', 'loan_date', 'is_returned')
    search_fields = ('book__title', 'user__username')
    list_filter = ('loan_date', 'return_date')
    ordering = ['-loan_date', 'book__title']
    actions = [mark_as_returned, mark_as_not_returned]
    raw_id_fields = ['user', 'book']


# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(Book, BookAdmin)
admin.site.register(BookDetail)
admin.site.register(Review)
admin.site.register(Recommendation)
# admin.site.register(Loan)

# Unregister the default User admin and register the custom one
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
