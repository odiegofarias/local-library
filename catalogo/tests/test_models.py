from django.test import TestCase
from django.urls import reverse
from catalogo.models import Author


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Author.objects.create(
            first_name='Diego',
            last_name='Fernandes'
        )

    def test_verifica_label_first_name(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name

        self.assertEqual(field_label, 'first name')
    
    def test_verifica_label_date_of_death(self):
        author = Author.objects.get(id=1)
        field_name = author._meta.get_field('date_of_death').verbose_name

        self.assertEqual(field_name, 'Died')
    
    def test_verifica_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name

        self.assertEqual(field_label, 'last name')
    
    def test_verifica_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name

        self.assertEqual(field_label, 'date of birth')

    def test_verifica_tamanho_do_campo_first_name(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length

        self.assertEqual(max_length, 30)
    
    def test_verifica_tamanho_do_campo_last_name(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length

        self.assertEqual(max_length, 30)

    def test_nome_do_objeto_eh_primeiro_nome_virgula_sobrenome(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.first_name}, {author.last_name}'

        self.assertEqual(expected_object_name, str(author))

    def test_a_url_renderizada_esta_correta(self):
        url = reverse('catalogo:author_detail', kwargs={'pk': 1})

        self.assertEqual(url, '/catalogo/author/1')