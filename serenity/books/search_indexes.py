# from haystack import indexes
# from .models import Book, Genre, Author, Summary

# class BookIndex(indexes.SearchIndex, indexes.Indexable):
#     title = indexes.CharField(model_attr='title')
#     author_name = indexes.CharField(model_attr='author__name')
#     author_bio = indexes.CharField(model_attr='author__bio')
#     genre_name = indexes.CharField(model_attr='genre__name')
#     summary_text = indexes.CharField(model_attr='summary__text')
#     isbn = indexes.CharField(model_attr='isbn')
#     text = indexes.CharField(document=True, use_template=False)

#     def get_model(self):
#         return Book

#     def index_queryset(self, using=None):
#         return self.get_model().objects.all()
