# coding=UTF-8
from django.db import models
from datetime import datetime
from rownodzien.books.models import BookInstance
from rownodzien.people.models import Librarian, Reader

class BookRent(models.Model):
    """
    Ta tabela określa wypożyczenia.

    Egzemplarz jest wypożyczony jeśli ma przynajmniej jedno wypożyczenie którego 
    pole real_due jest NULL (czyli jeszcze nie oddano)
    """
    bookinstance = models.ForeignKey(BookInstance, related_name='rentings')
    who = models.ForeignKey(Librarian, related_name='rentings')
    whom = models.ForeignKey(Reader, related_name='rentings')

    when_rented = models.DateTimeField(default=datetime.now, verbose_name=u'Kiedy wypożyczono')

    official_due = models.DateTimeField(verbose_name=u'Obliczona data oddania')
    real_due = models.DateTimeField(default=None, null=True, verbose_name=u'Rzeczywista dana oddania')
