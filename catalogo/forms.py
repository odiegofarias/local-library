import datetime
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from catalogo.models import BookInstance


class RenewBookForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back'] 
        labels = {'due_back': 'Data de renovação'}
        help_texts = {'due_back': 'Entre com uma data entre agora e 4 semanas (padrão: 3). '}

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError('Data inválida - A renovação está no passado')
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError('Data Inválida - Data de renovação maior do que 4 semanas')

        return data
