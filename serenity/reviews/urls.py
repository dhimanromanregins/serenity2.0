from django.urls import path
from . import views

urlpatterns = [
    path('review/submit/<int:book_id>/', views.submit_review, name='submit_review'),
    path('review/moderate/<int:review_id>/', views.moderate_review, name='moderate_review'),
]
