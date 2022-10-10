from django.http import HttpResponse
from django.shortcuts import render
from .models import *


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()
    # Pegando as instancias com status "A"

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_book_search = Book.objects.filter(title__icontains='e').count()
    print(num_book_search)
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_book_search': num_book_search,
    }

    return render(request, 'catalogo/index.html', context)
