from django.db import models
from django.db.models import Avg

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    summary = models.TextField()
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        ratings = self.reviews.filter(is_moderated=True).aggregate(Avg('rating'))['rating__avg']
        return round(ratings, 1) if ratings else None
