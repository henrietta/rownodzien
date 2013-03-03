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


