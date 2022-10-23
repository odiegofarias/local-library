from cgi import test
import datetime
from multiprocessing.connection import Client

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from catalogo.models import Author, Book, BookInstance, Genre, Language
from django.contrib.auth.models import User


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        number_of_authors = 14

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'Diego {author_id}',
                last_name=f'Fernandes {author_id}',
            )
    
    def test_view_url_existe_no_local_desejado(self):
        response = self.client.get('/catalogo/authors/')
        
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessivel_pelo_nome(self):
        response = self.client.get(reverse('catalogo:authors'))

        self.assertEqual(response.status_code, 200)

    def test_view_utilizando_o_template_correto(self):
        response = self.client.get(reverse('catalogo:authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo/author_list.html')

    def test_paginacao_da_pagina_1_esta_correta_retorna_5_autores(self):
        response = self.client.get(reverse('catalogo:authors')+'?page=1')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 5)

    def test_paginacao_da_pagina_2_esta_correta_retorna_5_autores(self):
        response = self.client.get(reverse('catalogo:authors')+'?page=2')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 5)
    
    def test_paginacao_da_pagina_3_esta_correta_retorna_4_autores(self):
        response = self.client.get(reverse('catalogo:authors')+'?page=3')

        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 4)

class LoadnedBookInstancesByUserListViewTest(TestCase):
    def setUp(self) -> None:
        # cria dois usuários
        test_user1 = User.objects.create(
            username='testuser1',
            password='tub4f5p2',
        )
        test_user2 = User.objects.create(
            username='testuser2',
            password='asdasdasdasd'
        )

        test_user1.save()
        test_user2.save()

        # Cria um livro
        test_author = Author.objects.create(
            first_name='Diego',
            last_name='Fernandes'
        )
        test_genre = Genre.objects.create(name='Fantasy')
        # test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title='Book title',
            summary='My Book summary',
            isbn='ABCDQWEQWEQWE',
            author=test_author,
            # language=test_language
        )

        # Cria gênero
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        # No many-to-many, não é permitido acessar direto
        test_book.save()

        # Cria 30 objetos BookInstances
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.localtime() + datetime.timedelta(days=book_copy%5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = 'm'
            
            BookInstance.objects.create(
                book=test_book,
                imprint='Inlikely Imprint, 2022',
                due_back=return_date,
                borrower=the_borrower,
                status=status,
            )



    def test_redirect_se_nao_estiver_logado(self):
        response = self.client.get(reverse('catalogo:my_borrowed'))

        self.assertRedirects(response, '/accounts/login/?next=/catalogo/mybooks/')
    




class LoginTest(TestCase):
    def test_login_como_anonimo_redireciona_para_url_login(self):
        url = self.client.get(reverse('catalogo:index'))
        self.assertRedirects(url, "/accounts/login/?next=/catalogo/")

    def test_apenas_usuarios_atenticados(self):
        user = User.objects.create_user(username='teste', password='teste_pass')
        self.client.force_login(user=user)
        url = self.client.get(reverse('catalogo:index'))
        
        self.assertEqual(url.status_code, 200)
        self.assertTemplateUsed(url, 'catalogo/index.html')
        self.assertIn('Local Library Home', url.content.decode('utf-8'))