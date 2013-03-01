# coding=UTF-8
"""Kontrolery obsługujące zarządzanie książkami"""
from django.shortcuts import redirect, get_object_or_404
from django import forms
from django.contrib import messages
import pyisbn

from rownodzien.main import render_to_response
from rownodzien.books.models import Book

class BookForm(forms.ModelForm):
    """Formularz służący do dodawania/edytowania książki"""
    class Meta:
        model = Book        # wzoruj formularz na tabeli Book

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']        # pobierz ISBN z formularza
        isbn = isbn.replace('-', '')            # usun pauzy

        # sprawdz czy to poprawny ISBN
        if not pyisbn.Isbn(isbn).validate():
            raise forms.ValidationError(u'Błędny ISBN')
        else:
            return isbn

def add_book(request):
    """Kontroler dodawania książki"""
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, u'Dodano książkę')
            return redirect('/book/%s/' % form.instance.isbn)

    return render_to_response('books/add.html', request, form=form)

def edit_book(request, isbn):
    """Kontroler edycji książki"""
    book = get_object_or_404(Book, isbn=isbn)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, u'Zmieniono książkę')
            return redirect('/book/%s/' % form.instance.isbn)

    return render_to_response('books/edit.html', request, form=form, book=book)

def delete_book(request, isbn):
    """Kontroler kasowania książki"""
    get_object_or_404(Book, isbn=isbn).delete()
    messages.add_message(request, messages.INFO, u'Usunięto książkę')
    return redirect('/')