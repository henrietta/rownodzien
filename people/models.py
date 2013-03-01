# coding=UTF-8
from django.db import models

class Reader(models.Model):
    """Ta tabela określa czytelników obecnych w systemie"""
    number = models.DecimalField(max_digits=4, decimal_places=0, verbose_name=u'Numer czytelnika')

    pesel = models.CharField(max_length=10, verbose_name=u'PESEL')
    name = models.CharField(max_length=50, verbose_name=u'Imię')
    surname = models.CharField(max_length=50, verbose_name=u'Nazwisko')
    phone = models.CharField(max_length=30, verbose_name=u'Telefon')

class Librarian(models.Model):
    """Ta tabela określa bibliotekarzy obecnych w systemie"""
    number = models.DecimalField(max_digits=4, decimal_places=0, verbose_name=u'Numer bibliotekarza')

    name = models.CharField(max_length=50, verbose_name=u'Imię')
    surname = models.CharField(max_length=50, verbose_name=u'Nazwisko')

    pesel = models.CharField(max_length=10, verbose_name=u'PESEL')