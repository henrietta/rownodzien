# Create your views here.
# coding=UTF-8

from django.shortcuts import render_to_response, get_object_or_404

from rownodzien.books.models import Book
from django.db.models import Count

"""Raport o dostępnych książkach"""
def report_books(request):
  books = Book.objects.all().annotate(Count('instances'))
  for book in books:
    liczba_wypozyczonych = 0
    for instance in book.instances.all():
      if (instance.is_rented() and instance.is_damaged == 0 and instance.is_lost == 0):
        liczba_wypozyczonych += 1
    book.dostepne = book.instances.count() - liczba_wypozyczonych
  return render_to_response('reports/books.html', {'book': books})

from rownodzien.books.models import BookInstance

"""Raport o dostępnych egzemplarzach"""
def report_instances(request):
	instances = BookInstance.objects.all()
	return render_to_response('reports/instances.html', {'instance': instances})

from rownodzien.rentings.models import BookRent

"""Raport o aktualnych wypożyczeniach"""
def report_rentings(request):
  rentings = BookRent.objects.filter(real_due__exact=None)
  return render_to_response('reports/rentings.html', {'renting': rentings})

"""Raport o historii wypożyczeń"""
def report_rentingshistory(request):
  rentings = BookRent.objects.all()
  return render_to_response('reports/rentings_history.html', {'renting': rentings})

from rownodzien.people.readers import Reader

"""Raport o czytelnikach"""
def report_readers(request):
  readers = Reader.objects.all().annotate(Count('rentings'))
  for reader in readers:
    aktualne = reader.rentings.filter(real_due__exact=None).count()
    reader.aktualne = aktualne
  return render_to_response('reports/readers.html', {'reader': readers})

"""Zwracanie wypożyczonych książek przez czytelnika"""
def report_returnbyreader(request, pesel):
  reader = get_object_or_404(Reader, pesel=pesel)
  rents = []
  insts = []

  for renting in BookRent.objects.all():
    if (renting.whom == reader and renting.real_due == None):
      rents.append(renting)
      for instance in BookInstance.objects.all():
        if instance == renting.bookinstance:
          insts.append(instance)
          continue

  return render_to_response('reports/return_by_reader.html', {'reader': reader, 'rentings': rents, 'instances': insts})

"""Zwracanie dostępnych egzemplarzy danej książki"""
def report_avainstances(request, isbn):
  book = get_object_or_404(Book, isbn=isbn)
  insts = []

  for instance in BookInstance.objects.all():
    if (instance.book == book and instance.is_rented() == 0 and instance.is_damaged == 0 and instance.is_lost == 0):
      insts.append(instance)

  return render_to_response('reports/ava_instances.html', {'book': book, 'instances': insts})