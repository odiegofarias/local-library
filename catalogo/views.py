from django.shortcuts import get_object_or_404, render
from .models import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required


@login_required(login_url="login", redirect_field_name="next")
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()
    # Pegando as instancias com status "A"

    # Pegando as sessions
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_book_search = Book.objects.filter(title__icontains='a').count()
    print(num_book_search)
    num_authors = Author.objects.count()


    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_book_search': num_book_search,
        'num_visits': num_visits,
    }

    return render(request, 'catalogo/index.html', context)


class BookList(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    paginate_by = 6

# def book_list(request):
#     list_book = Book.objects.all()

#     context = {
#         'list_book': list_book
#     }

#     return render(request, 'catalogo/book_list.html', context)


# class BookDetailView(generic.DetailView):
#     model = Book
#     context_object_name = 'book_detail'



def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(
        request,
        'catalogo/book_detail.html',
        {'book': book},
    )


class AuthorsList(LoginRequiredMixin, generic.ListView):
    login_url = 'login'
    redirect_field_name = 'next'
    model = Author
    context_object_name = 'author_list'


# def authors_list_view(request):
#     books = Book.objects.all()
#     authors = Author.objects.all()

#     context = {
#         'books': books,
#         'authors': authors,
#     }

#     return render(
#         request,
#         'catalogo/author_list.html',
#         context,
#     )

class AuthorsDetail(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalogo/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        # return BookInstance.objects.filter(
        #     borrower=self.request.user
        # ).filter(status__exact='o').order_by('due_back')
        return BookInstance.objects.all()


@login_required(login_url="login", redirect_field_name="next")
def livro_emprestado(request):
    book_list_user = BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').order_by('due_back')
    book_list_staff = BookInstance.objects.all()

    context = {
        'book_list_staff': book_list_staff,
        'book_list_user': book_list_user,
    }

    return render(request, 'catalogo/bookinstance_list_borrowed_user.html', context)


class TodosEmprestimosView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalogo'
        


