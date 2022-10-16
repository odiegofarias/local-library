from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import datetime
from catalogo.forms import RenewBookForm
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



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
    paginate_by = 12

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
        

@permission_required('catalogo.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = BookInstance.objects.get(pk=pk)

    if request.method == "POST":
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            return redirect('catalogo:my_borrowed')

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance
    }
    
    return render(request, 'catalogo/book_renew_librarian.html', context)


class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}
    success_url = reverse_lazy('catalogo:authors')


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    success_url = reverse_lazy('catalogo:authors')

class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('catalogo:authors')


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('catalogo:books')


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('catalogo:books')


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('catalogo:books')

