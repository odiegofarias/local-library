from django.urls import path, include
from . import views


app_name = 'catalogo'

urlpatterns = [
    path('', views.index, name="index"),
    path('books/', views.BookList.as_view(), name="books"),
    path('book/<int:pk>', views.book_detail_view, name='book_detail'),
    path('authors/', views.AuthorsList.as_view(), name="authors"),
    path('authors/<int:pk>', views.AuthorsDetail.as_view(), name="author_detail"),
    path('mybooks/', views.livro_emprestado, name='my_borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew_book_librarian'),
] 
    
