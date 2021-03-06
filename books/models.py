# coding=UTF-8
from django.db import models
from datetime import datetime
from rownodzien.people.models import Librarian, Reader
from urllib import quote_plus as urlquote

class Book(models.Model):
    """Ta tabela określa książki dostępne w systemie"""
    author = models.CharField(blank=True, max_length=40, verbose_name=u'Autor')
    title = models.CharField(blank=True, max_length=40, verbose_name=u'Tytuł')
    year = models.IntegerField(blank=True, null=True, verbose_name=u'Rok wydania')
    isbn = models.CharField(blank=True, max_length=13, unique=True, verbose_name=u'ISBN')
    publish_place = models.CharField(blank=True, max_length=40, verbose_name=u'Miejsce wydania')
   
    year_pl = models.IntegerField(blank=True, null=True, verbose_name=u'Rok wydania polskiego')
    language = models.CharField(blank=True, default=u'Polski', max_length=20, verbose_name=u'Język')
    translation = models.CharField(blank=True, max_length=40, verbose_name=u'Przekład')

    class Meta:
        verbose_name = u'książkach'

    def get_absolute_url(self):
        """Zwraca adres URL dla tego modelu"""
        return '/book/%s/' % self.isbn

class BookInstance(models.Model):
    """Ta tabela określa egzemplarze książek dostępne w systemie"""
    book = models.ForeignKey(Book, related_name='instances', verbose_name=u'Książka')

    code = models.CharField(max_length=14, unique=True, verbose_name=u'Nr lub kod kreskowy')

    is_damaged = models.BooleanField(default=False, verbose_name=u'Czy uszkodzona ?')
    is_lost = models.BooleanField(default=False, verbose_name=u'Czy zagubiona?')

    def get_absolute_url(self):
        """Zwraca adres URL dla tego modelu"""
        return '/instance/%s/' % urlquote(self.code)

    def is_rented(self):
        """
        Zwraca czy książka jest wypożyczona.

        Książka jest wypożyczona jeśli ma jeden rekord BookRent którego
        pole real_due wynosi NULL

        @return: bool
        """
        return self.rentings.filter(real_due__isnull=True).count() == 1

    def get_renting(self):
        """
        Zwraca obiekt BookRent który dotyczy aktualnego wypożyczenia książki.

        Rzuca ValueError jeśli książka nie jest wypożyczona
        """
        try:
            return self.rentings.get(real_due__isnull=True)
        except:
            raise ValueError, u'Książka nie jest wypożyczona'
