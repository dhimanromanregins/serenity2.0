from django_elasticsearch_dsl import Document, fields, Index
from django_elasticsearch_dsl.registries import registry
from .models import Book, Genre

# Define the Elasticsearch index
book_index = Index('books')

# Set the settings for the index
book_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

# Define the document
@book_index.doc_type
class BookDocument(Document):
    genre = fields.ObjectField(properties={
        'name': fields.TextField(),
    })

    class Django:
        model = Book
        fields = [
            'title',
            'author',
            'isbn',
            'summary',
        ]
