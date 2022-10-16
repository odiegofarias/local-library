import datetime

from django.test import TestCase, SimpleTestCase
from django.utils import timezone

from catalogo.forms import RenewBookForm


class RenewBookFormTest(SimpleTestCase):
    def test_renew_form_date_campo_label(self):
        form = RenewBookForm()

        self.assertTrue(form.fields['due_back'].label == None or form.fields['due_back'].label == 'Data de renovação')

    def test_renew_form_date_campo_help_text(self):
        form = RenewBookForm()

        self.assertEqual(form.fields['due_back'].help_text, 'Entre com uma data entre agora e 4 semanas (padrão: 3). ')

    def test_renew_form_date_no_passado(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'due_back': date})

        self.assertFalse(form.is_valid())

    def test_renw_form_date_acima_de_4_semanas(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'due_back': date})

        self.assertFalse(form.is_valid())

    def test_renew_form_date_eh_hoje(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'due_back': date})

        self.assertTrue(form.is_valid())

    def test_renew_form_date_nao_excede_data_maxima(self):
        date = timezone.localdate() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'due_back': date})

        self.assertTrue(form.is_valid())

