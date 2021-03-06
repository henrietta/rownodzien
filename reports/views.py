# Create your views here.
# coding=UTF-8

from django.shortcuts import render_to_response, get_object_or_404

from rownodzien.books.models import Book
from django.db.models import Count

"""Raport o dostępnych książkach"""
def report_books(request, before_1980=False):
  books = Book.objects.all().annotate(Count('instances'))
  if before_1980:
    books = books.filter(year__lt=1980)
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

  rents = BookRent.objects.filter(real_due__exact=None).filter(whom=reader)

  return render_to_response('reports/return_by_reader.html', {'reader': reader, 'instances': rents})

"""Zwracanie dostępnych egzemplarzy danej książki"""
def report_avainstances(request, isbn):
  book = get_object_or_404(Book, isbn=isbn)
  insts = []

  insts = BookInstance.objects.filter(book=book).filter(is_damaged=False).filter(is_lost=False)
  insts = [instance for instance in insts if not instance.is_rented()]

  return render_to_response('reports/ava_instances.html', {'book': book, 'instances': insts})