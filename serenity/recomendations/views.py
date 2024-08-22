from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import  UserGenre, UserIntrests
from .forms import UserGenreForm
from books.models import Genre, Book
from django.db.models import Q



@login_required
def select_genres(request):
    if request.method == 'POST':
        form = UserGenreForm(request.POST)
        if form.is_valid():
            UserGenre.objects.filter(user=request.user).delete()
            for genre in form.cleaned_data['genres']:
                UserGenre.objects.create(user=request.user, name=genre.name)
            return redirect('genre_success')
    else:
        form = UserGenreForm()

    return render(request, 'recomendations/gener_select.html', {'form': form})


def genre_success(request):
    return render(request, 'recomendations/genre_success.html')




@login_required
def recomended_books(request):
    user = request.user
    user_interests = UserIntrests.objects.filter(user=user)
    user_genres = UserGenre.objects.filter(user=user)
    books = Book.objects.none()
    if user_genres.exists():
        genre_names = [user_genre.name for user_genre in user_genres]
        books = Book.objects.filter(genre__name__in=genre_names)
    queries = [interest.text for interest in user_interests]
    query_filters = Q()
    for query in queries:
        query_filters |= Q(title__icontains=query) | Q(isbn__icontains=query) | Q(author__name__icontains=query) | Q(author__bio__icontains=query) | Q(summary__text__icontains=query)

    if queries:
        books = books.filter(query_filters)

    books_by_genre = {}
    if books.exists():
        for book in books:
            genre = book.genre.name
            if genre not in books_by_genre:
                books_by_genre[genre] = []
            books_by_genre[genre].append(book)
    genres = Genre.objects.all()

    return render(request, 'recomendations/recomended_books.html', {
        'books_by_genre': books_by_genre,
        'genres': genres,
        'selected_genre': request.GET.get('genre', ''),
    })
