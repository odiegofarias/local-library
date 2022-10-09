import uuid
from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Entre com o gênero do livro(ex: Ficção Cietífica)'
    )

    def __str__(self) -> str:
        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Entre com a lingua do livro (ex: English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000,
        help_text='Entre com uma breve descrição do livro'
    )
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        help_text='13 caractéres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
    )
    genre = models.ManyToManyField(
        Genre,
        help_text='Escolha o gênero do livro',
    )

    def __str__(self) -> str:
        return self.title

    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='ID exclusivo para este livro específico em toda a biblioteca',
    )
    book = models.ForeignKey(
        'Book',
        on_delete=models.SET_NULL,
        null=True,
    )
    imprint = models.CharField(max_length=200)
    # devolvido
    due_back = models.DateField(null=True, blank=True)
    #  Pessoa que pegou o empréstimo do livro
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    @property
    def is_overdue(self):
        """Determina se o livro está vencido com base na data de vencimento e na data atual."""
        return bool(self.due_back and date.today() > self.due_back)

    # status de emprestimo do livro
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Disponibilidade do livro'
    )

    class Meta:
        ordering = ['due_back']


    def __str__(self) -> str:
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self) -> str:
        return f'{self.first_name}, {self.last_name}'
    
    
