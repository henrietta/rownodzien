# coding=UTF-8
"""Kontrolery obsługujące zarządzanie czytelnikami"""
from django.shortcuts import redirect, get_object_or_404
from django import forms
from django.contrib.localflavor.pl.forms import PLPESELField
from django.contrib import messages
from decimal import Decimal

from rownodzien.people.models import Librarian, get_unique_number
from rownodzien.main import sysfault, render_to_response

class LibrarianForm(forms.ModelForm):
    """Formularz służący do dodawania/edycji bibliotekarza"""
    class Meta:
        model = Librarian        # wzoruj formularz na tabeli Book
        exclude = ('number', )  # number jest automatycznie generowany

    pesel = PLPESELField()

def add_librarian(request):
    """Kontroler dodawania bibliotekarza"""
    form = LibrarianForm()

    if request.method == 'POST':
        form = LibrarianForm(request.POST)
        if form.is_valid():
            try:
                form.instance.number = get_unique_number(Librarian)
            except ValueError:
                return sysfault(u"""Nie można nadać bibliotekarzowi unikatowego numeru
                                  czterocyfrowego. Wszystkie numery są już zajęte. Problem
                                  ten wynika z specyfikacji tejże bazy danych i można 
                                  go tylko naprawić kasując istniejących bibliotekarzy""")
            form.save()
            messages.add_message(request, messages.INFO, u'Dodano bibliotekarza')
            return redirect('/librarian/%s/' % form.instance.number)

    return render_to_response('librarians/add.html', request, form=form)

def edit_librarian(request, number):
    """Kontroler edycji bibliotekarza"""
    instance = get_object_or_404(Librarian, number=Decimal(number))
    form = LibrarianForm(instance=instance)

    if request.method == 'POST':
        form = LibrarianForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, u'Zmieniono czytelnika')
            return redirect('/librarian/%s/' % form.instance.number)

    return render_to_response('librarians/edit.html', request, form=form, librarian=instance)

def delete_librarian(request, number):
    """Kontroler kasowania czytelnika"""
    get_object_or_404(Librarian, number=Decimal(number)).delete()
    messages.add_message(request, messages.INFO, u'Usunięto bibliotekarza')
    return redirect('/')