from django.contrib import admin
from . import models


class BooksInstanceInline(admin.TabularInline):
    model = models.BookInstance


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'date_of_birth',
        'date_of_death',
    )
    fields = ['first_name', 'last_name',
    #  Mostra horizontalmente
    ('date_of_birth', 'date_of_death'),
    ]


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    ...


@admin.register(models.BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),

        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
