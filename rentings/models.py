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
    bookinstance = models.ForeignKey(BookInstance, related_name='rentings', verbose_name=u'Egzemplarz')
    who = models.ForeignKey(Librarian, related_name='rentings', verbose_name=u'Kto wypożycza')
    whom = models.ForeignKey(Reader, related_name='rentings', verbose_name=u'Komu wypożycza')

    when_rented = models.DateTimeField(default=datetime.now, verbose_name=u'Kiedy wypożyczono')

    official_due = models.DateTimeField(verbose_name=u'Obliczona data oddania')
    real_due = models.DateTimeField(default=None, null=True, verbose_name=u'Rzeczywista dana oddania')


    def close(self, was_damaged=False, was_lost=False):
        """
        Rejestruje zwrot na danym wypożyczeniu.

        Flagi podane jako parametr będą naniesione na egzemplarz. Ta
        metoda zapisuje model ten i swojego egzemplarza.

        @param was_damaged: Czy książka została oddana zniszczona
        @param was_lost: Czy zwrot jest zwrotem wirtualnym, służącym rejestrowaniu
            zagubionego egzemplarza
        """
        if was_damaged:
            self.bookinstance.is_damaged = True
        if was_lost:
            self.bookinstance.is_lost = True
        self.bookinstance.save()

        self.real_due  = datetime.now()
        self.save()
