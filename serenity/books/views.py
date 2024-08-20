from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Genre
from .forms import BookForm
from django.views.generic import ListView, DetailView
from django.db.models import Q


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get search query and selected genre from request
        search_query = self.request.GET.get('q', '')
        selected_genre = self.request.GET.get('genre', '')

        # Apply search filter to text fields only
        if search_query:
            search_filter = (
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(isbn__icontains=search_query) |
                Q(summary__icontains=search_query)  # Include other text fields if needed
            )
            queryset = queryset.filter(search_filter)

        # Apply genre filter using ForeignKey relationship
        if selected_genre:
            queryset = queryset.filter(genre__id=selected_genre)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all genres to populate the dropdown
        context['genres'] = Genre.objects.all()
        # Pass the current search query and selected genre to the template
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_genre'] = self.request.GET.get('genre', '')
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.filter(is_moderated=True)
        return context


def add_or_edit_book(request, pk=None):
    if pk:
        book = get_object_or_404(Book, pk=pk)
    else:
        book = None

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'books/book_form.html', {'form': form})


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})


def patch_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)

    form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})


def search_books(request):
    query = request.GET.get('q')
    genre_id = request.GET.get('genre', '')

    print(query, '-------------------------')

    books = Book.objects.all()

    # Apply search filters
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(
            author__icontains=query) | Book.objects.filter(genre__icontains=query) | Book.objects.filter(
            isbn__icontains=query)
    else:
        books = Book.objects.all()

    # Filter by genre if selected
    if genre_id:
        try:
            genre = Genre.objects.get(id=genre_id)
            books = books.filter(genre=genre)
        except Genre.DoesNotExist:
            books = books.none()  # Return an empty queryset if genre doesn't exist

    genres = Genre.objects.all()

    return render(request, 'books/search_results.html', {
        'books': books,
        'genres': genres,
        'selected_genre': genre_id,
        'search_query': query
    })