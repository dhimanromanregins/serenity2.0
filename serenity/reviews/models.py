from django.db import models
from django.conf import settings
from books.models import Book

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_moderated = models.BooleanField(default=False)  # To track if a review has been moderated

    def __str__(self):
        return f"Review by {self.user} for {self.book.title}"
