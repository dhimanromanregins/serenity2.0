from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Genre
from .forms import BookForm
from .search_indexes import BookDocument
from django.views.generic import ListView, DetailView


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'


def add_or_edit_book(request, pk=None):
    if pk:
        book = get_object_or_404(Book, pk=pk)
    else:
        book = None

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
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
    genre_id = request.GET.get('genre')
    
    books = BookDocument.search().filter('match_all')

    if query:
        books = books.query("multi_match", query=query, fields=['title', 'author', 'isbn', 'summary', 'genre.name'])

    if genre_id:
        genre = Genre.objects.get(id=genre_id)
        books = books.filter('term', genre__name=genre.name)
    
    genres = Genre.objects.all()
    
    return render(request, 'books/search_results.html', {'books': books, 'genres': genres, 'selected_genre': genre_id, 'search_query': query})
