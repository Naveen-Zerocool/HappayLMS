from django.urls import path

from book_store import views


urlpatterns = [
    path('authors/', views.AuthorView.as_view(),
         name='authors'),
    path('authors/<uuid:author_id>/', views.AuthorView.as_view(),
         name='individual-author'),

    path('categories/', views.CategoryView.as_view(),
         name='categories'),
    path('categories/<uuid:category_id>/', views.CategoryView.as_view(),
         name='individual-category'),

    path('books/search/', views.BookSearchView.as_view(),
         name='search-books'),

    path('books/', views.BookView.as_view(),
         name='individual-book'),
]
