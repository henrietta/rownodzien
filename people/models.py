# coding=UTF-8
from django.db import models

class Reader(models.Model):
    """Ta tabela określa czytelników obecnych w systemie"""
    number = models.DecimalField(max_digits=4, decimal_places=0, unique=True, verbose_name=u'Numer czytelnika')

    pesel = models.CharField(max_length=11, verbose_name=u'PESEL', unique=True)
    name = models.CharField(max_length=50, verbose_name=u'Imię')
    surname = models.CharField(max_length=50, verbose_name=u'Nazwisko')
    phone = models.CharField(max_length=30, verbose_name=u'Telefon')

    def __unicode__(self):
        return u'#%s %s %s' % (self.number, self.name, self.surname)

class Librarian(models.Model):
    """Ta tabela określa bibliotekarzy obecnych w systemie"""
    number = models.DecimalField(max_digits=4, decimal_places=0, unique=True, verbose_name=u'Numer bibliotekarza')

    name = models.CharField(max_length=50, verbose_name=u'Imię')
    surname = models.CharField(max_length=50, verbose_name=u'Nazwisko')

    pesel = models.CharField(max_length=11, verbose_name=u'PESEL')

    def __unicode__(self):
        return u'#%s %s %s' % (self.number, self.name, self.surname)


def get_unique_number(model):
    """
    Generuje unikatowy numer Number dla danego typu modelu.
    Numer będzie maksymalnie czterocyfrowy. Jeśli nie uda się
    znaleźć wolnego numeru, zostanie wyrzucony wyjątek
    ValueError.

    @param model: model, typ Reader lub Librarian
    @return: int, sugerowany czterocyfrowy numer
    """

    # Zastosuj podejście naiwne - o 1 większy niż maksimum
    id_max = model.objects.all().aggregate(models.Max('number'))['number__max']

    if id_max == None:  # nie istnieje żaden obiekt tego typu
        return 1    # bezpiecznie możemy zwrócić 1

    if str(id_max+1) <= 4:  # jeśli powiększony o 1 ma 4 cyfry..
        return id_max+1 # to może zostać zwrócony.

    # Jesteśmy w sytuacji skrajnej, musimy przeglądnąć tabelę w poszukiwaniu
    # wolnych numerów
    allnums = [int(x.number) for x in model.objects.all().only('number')]

    for x in xrange(1, 10000):
        if x not in allnums:
            return x    # x to dostępny numer

    raise ValueError, u'Nie można zaalokować numeru'    