# coding=UTF-8
"""Kontrolery obsługujące zarządzanie książkami"""
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django import forms
from django.contrib import messages
from urllib import quote_plus as urlquote

from rownodzien.books.models import BookInstance, Book


class BookInstanceForm(forms.ModelForm):
    """Formularz służący do dodawania/edytowania egzemplarza"""
    class Meta:
        model = BookInstance        # wzoruj formularz na tabeli BookInstance
        exclude = ('book', ) # nie wyświetlaj pola book

def add_instance(request, isbn):
    """Kontroler dodawania egzemplarza"""
    book = get_object_or_404(Book, isbn=isbn)
    form = BookInstanceForm()

    if request.method == 'POST':
        form = BookInstanceForm(request.POST)
        if form.is_valid():
            form.instance.book = book
            form.save()
            messages.add_message(request, messages.INFO, u'Dodano egzemplarz')
            return redirect('/instance/%s/' % urlquote(form.instance.code))

    return render_to_response('instances/add.html', {'request': request,
                                                     'form': form,
                                                     'book': book})

def edit_instance(request, code):
    """Kontroler edycji egzemplarza"""
    instance = get_object_or_404(BookInstance, code=code)
    form = BookInstanceForm(instance=instance)

    if request.method == 'POST':
        form = BookInstanceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            cd = form.instance.code
            messages.add_message(request, messages.INFO, u'Zmieniono egzemplarz')
            return redirect('/instance/%s/' % urlquote(form.instance.code))

    return render_to_response('instances/edit.html', {'request': request,
                                                      'form': form,
                                                      'instance': instance})

def delete_instance(request, code):
    """Kontroler kasowania egzemplarza"""
    instance = get_object_or_404(BookInstance, code=code)
    bookisbn = instance.book.isbn
    instance.delete()
    messages.add_message(request, messages.INFO, u'Usunięto egzemplarz')
    return redirect('/book/%s/' % bookisbn)