# coding=UTF-8
from django.db import models
from datetime import datetime
from rownodzien.people.models import Librarian, Reader

class Book(models.Model):
    """Ta tabela określa książki dostępne w systemie"""
    author = models.CharField(max_length=40, verbose_name=u'Autor')
    title = models.CharField(max_length=40, verbose_name=u'Tytuł')
    year = models.IntegerField(verbose_name=u'Rok wydania')

    isbn = models.CharField(max_length=13, unique=True, verbose_name=u'ISBN')

    class Meta:
        verbose_name = u'książkach'

class BookInstance(models.Model):
    """Ta tabela określa egzemplarze książek dostępne w systemie"""
    book = models.ForeignKey(Book, related_name='instances', verbose_name=u'Książka')

    code = models.CharField(max_length=14, unique=True, verbose_name=u'Nr lub kod kreskowy')

    is_damaged = models.BooleanField(default=False, verbose_name=u'Czy uszkodzona?')
    is_lost = models.BooleanField(default=False, verbose_name=u'Czy zagubiona?')

    def is_rented(self):
        """
        Zwraca czy książka jest wypożyczona.

        Książka jest wypożyczona jeśli ma jeden rekord BookRent którego
        pole real_due wynosi NULL

        @return: bool
        """
        return self.rentings.filter(real_due__isnull=True).count() == 1

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


