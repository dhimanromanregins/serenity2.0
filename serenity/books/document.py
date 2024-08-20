from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Book, Author, Genre, Summary

@registry.register_document
class BookDocument(Document):
    author = fields.ObjectField(properties={
        'name': fields.TextField(),
        'bio': fields.TextField(),
    })
    genre = fields.ObjectField(properties={
        'name': fields.TextField(),
    })
    summary = fields.ObjectField(properties={
        'book_title': fields.TextField(),
        'text': fields.TextField(),
    })
    title = fields.TextField()
    isbn = fields.TextField()
    published_date = fields.DateField()
    image = fields.TextField()  # Assuming image is a URL or path

    class Index:
        name = 'books'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Book
        fields = []  # No need to include fields here since they're defined above
