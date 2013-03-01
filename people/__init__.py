# coding=UTF-8
from django.db.models import Max

from rownodzien.people.models import Reader, Librarian

def suggest_unique_number(model):
    """
    Sugeruje unikatowy numer Number dla danego typu modelu.
    Numer będzie maksymalnie czterocyfrowy. Jeśli nie uda się
    znaleźć wolnego numeru, zostanie wyrzucony wyjątek
    ValueError.

    @param model: model, typ Reader lub Librarian
    @return: int, sugerowany czterocyfrowy numer
    """

    # Zastosuj podejście naiwne - o 1 większy niż maksimum
    id_max = model.objects.all().aggregate(Max('number'))['number__max']

    if id_max == None:  # nie istnieje żaden obiekt tego typu
        return 1    # bezpiecznie możemy zwrócić 1

    if str(id_max+1) <= 4:  # jeśli powiększony o 1 ma 4 cyfry..
        return id_max+1 # to może zostać zwrócony.

    # Jesteśmy w sytuacji skrajnej, musimy przeglądnąć tabelę w poszukiwaniu
    # wolnych numerów
    allnums = [int(x.number) for x in list(model.objects.all().only('number'))]

    for x in xrange(1, 10000):
        if x not in allnums:
            return x    # x to dostępny numer

    raise ValueError, u'Nie można zaalokować numeru'