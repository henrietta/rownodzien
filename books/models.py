# coding=UTF-8
from django.db import models
from datetime import datetime
from rownodzien.people.models import Librarian, Reader

class Book(models.Model):
    author = models.CharField(max_length=40)
    title = models.CharField(max_length=40)
    year = models.IntegerField()

    isbn = models.CharField(max_length=13, null=True)

class BookInstance(models.Model):
    book = models.ForeignKey(Book, related_name='instances', verbose_name=u'Książka')

    code = models.CharField(max_length=14, verbose_name=u'Nr lub kod kreskowy')

    is_damaged = models.BooleanField(default=False, verbose_name=u'Czy uszkodzona?')
    is_lost = models.BooleanField(default=False, verbose_name=u'Czy zagubiona?')

class BookRent(models.Model):
    bookinstance = models.ForeignKey(BookInstance, related_name='rentings')
    who = models.ForeignKey(Librarian, related_name='rentings')
    whom = models.ForeignKey(Reader, related_name='rentings')

    when_rented = models.DateTimeField(default=datetime.now, verbose_name=u'Kiedy wypożyczono')

    official_due = models.DateTimeField(verbose_name=u'Obliczona data oddania')
    real_due = models.DateTimeField(default=None, null=True, verbose_name=u'Rzeczywista dana oddania')


