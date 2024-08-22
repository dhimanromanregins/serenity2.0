from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import  UserGenre, UserIntrests
from .forms import UserGenreForm
from books.models import Genre, Book
from elasticsearch_dsl import Search

@login_required
def select_genres(request):
    if request.method == 'POST':
        form = UserGenreForm(request.POST)
        if form.is_valid():
            # Clear previous user genre selections
            UserGenre.objects.filter(user=request.user).delete()

            # Save new genre selections
            for genre in form.cleaned_data['genres']:
                UserGenre.objects.create(user=request.user, name=genre.name)

            return redirect('genre_success')  # Redirect to a success page or any other page
    else:
        form = UserGenreForm()

    return render(request, 'recomendations/gener_select.html', {'form': form})


def genre_success(request):
    return render(request, 'recomendations/genre_success.html')




@login_required
def recomended_books(request):
    user = request.user

    # Retrieve user interests and genres
    user_interests = UserIntrests.objects.filter(user=user)
    user_genres = UserGenre.objects.filter(user=user)

    # Initialize books queryset
    books = Book.objects.none()

    if user_genres.exists():
        genre_names = [user_genre.name for user_genre in user_genres]
        books = Book.objects.filter(genre__name__in=genre_names)

    # Collect queries from user interests
    queries = [interest.text for interest in user_interests]

    if queries:
        s = Search(index='books').query(
            'multi_match',
            query=" ".join(queries),
            fields=['title', 'author.name', 'genre.name', 'summary.text', 'isbn']
        )
        search_results = s.execute()
        ids = [hit.meta.id for hit in search_results]
        books = books.filter(id__in=ids)

    # Group books by genre
    books_by_genre = {}
    if books.exists():
        for book in books:
            genre = book.genre.name
            if genre not in books_by_genre:
                books_by_genre[genre] = []
            books_by_genre[genre].append(book)

    # Get all genres for the dropdown
    genres = Genre.objects.all()

    return render(request, 'recomendations/recomended_books.html', {
        'books_by_genre': books_by_genre,
        'genres': genres,
        'selected_genre': request.GET.get('genre', ''),
    })
