from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from books.models import Book

@login_required
def submit_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', pk=book_id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/submit_review.html', {'form': form, 'book': book})

@login_required
def moderate_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if not request.user.is_superuser:
        return redirect('book_list')  # Only allow admins to moderate
    if request.method == 'POST':
        if 'delete' in request.POST:
            review.delete()
        elif 'edit' in request.POST:
            # Implement edit functionality if needed
            pass
        return redirect('book_list')
    return render(request, 'reviews/moderate_review.html', {'review': review})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.filter(is_moderated=True).order_by('-created_at')
    return render(request, 'books/book_detail.html', {'book': book, 'reviews': reviews})


