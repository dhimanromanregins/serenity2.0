from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Genre
from .forms import BookForm
from django.views.generic import ListView, DetailView
from audiobooks.models import Audiobook
from django.db.models import Q, Exists, OuterRef
from dashboard.models import ReadingHistory, RecentlyViewed, SaveBook
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .document import BookDocument
from django_elasticsearch_dsl.search import Search
from .utils import synthesize_speech
from django.conf import settings


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get search query, selected genre, and audiobook filter from request
        search_query = self.request.GET.get('q', '')
        selected_genre = self.request.GET.get('genre', '')
        has_audiobook = self.request.GET.get('has_audiobook', '') == 'on'

        # Apply search filter with Elasticsearch
        if search_query:
            s = Search(index='books').query(
                'multi_match',
                query=search_query,
                fields=['title', 'author.name', 'genre.name', 'summary.book_title', 'summary.text', 'isbn']
            )
            search_results = s.execute()
            ids = [hit.meta.id for hit in search_results]
            queryset = queryset.filter(id__in=ids)

        # Apply genre filter
        if selected_genre:
            queryset = queryset.filter(genre__id=selected_genre)

        # Apply audiobook filter
        if has_audiobook:
            queryset = queryset.filter(audiobooks__isnull=False).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all genres to populate the dropdown
        context['genres'] = Genre.objects.all()
        # Pass the current search query and selected genre to the template
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_genre'] = self.request.GET.get('genre', '')
        context['has_audiobook'] = self.request.GET.get('has_audiobook', '') == 'on'

        if self.request.user.is_authenticated:
            recently_viewed = RecentlyViewed.objects.filter(user=self.request.user).select_related('book')
            context['recently_viewed'] = recently_viewed
            saved_books = SaveBook.objects.filter(user=self.request.user).select_related('book')
            context['saved_books'] = saved_books

            # Get reading history
            reading_history = ReadingHistory.objects.filter(user=self.request.user).select_related('book')
            context['reading_history'] = reading_history
        return context



class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch all reviews related to the book that are moderated
        context['reviews'] = self.object.reviews.filter(is_moderated=True)

        # Get all audiobooks related to this book
        audiobooks = self.object.audiobooks.all()
        context['audiobooks'] = audiobooks

        # Extract unique narrators from the audiobooks
        narrators = audiobooks.values_list('narrator', flat=True).distinct()
        context['narrators'] = narrators

        # Get selected narrator from the request (if any)
        selected_narrator = self.request.GET.get('narrator')
        context['selected_narrator'] = selected_narrator

        # Filter audiobooks by selected narrator if any narrator is selected
        if selected_narrator:
            context['filtered_audiobooks'] = audiobooks.filter(narrator=selected_narrator)
        else:
            context['filtered_audiobooks'] = audiobooks

        if self.request.user.is_authenticated:
            context['is_saved'] = SaveBook.objects.filter(user=self.request.user, book=self.object).exists()
        else:
            context['is_saved'] = False

        # Handle voice selection and generate audio
        # selected_voice = self.request.POST.get('voice',
        #                                        'en-US-Wavenet-D')  # Default to a specific voice if not selected
        # context['selected_voice'] = selected_voice

        # summary_text = self.object.summary.text
        # audio_filename = f"{self.object.id}_summary_{selected_voice}.mp3"
        # audio_file_path = synthesize_speech(summary_text, audio_filename, selected_voice)
        # context['audio_file_url'] = settings.MEDIA_URL + 'text-to-speech/' + audio_filename

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


def generate_audio(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        selected_voice = request.POST.get('voice', 'en-US-Wavenet-D')
        summary_text = book.summary.text
        audio_filename = f"{book.id}_summary_{selected_voice}.mp3"
        synthesize_speech(summary_text, audio_filename, selected_voice)
    return redirect('book_detail', pk=pk)


@login_required
def save_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    SaveBook.objects.get_or_create(user=request.user, book=book)
    return redirect('book_detail', pk=book.id)  # Use pk here

@login_required
def unsave_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    saved_book = SaveBook.objects.filter(user=request.user, book=book)
    if saved_book.exists():
        saved_book.delete()
    return redirect('book_detail', pk=pk)