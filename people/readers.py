# coding=UTF-8
"""Kontrolery obsługujące zarządzanie czytelnikami"""
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django import forms
from django.contrib.localflavor.pl.forms import PLPESELField
from django.contrib import messages
from decimal import Decimal

from rownodzien.people.models import Reader, get_unique_number
from rownodzien.main import sysfault

class ReaderForm(forms.ModelForm):
    """Formularz służący do dodawania/edycji czytelnika"""
    class Meta:
        model = Reader        # wzoruj formularz na tabeli Book
        exclude = ('number', )  # number jest automatycznie generowany

    pesel = PLPESELField()

def add_reader(request):
    """Kontroler dodawania czytelnika"""
    form = ReaderForm()

    if request.method == 'POST':
        form = ReaderForm(request.POST)
        if form.is_valid():
            try:
                form.instance.number = get_unique_number(Reader)
            except ValueError:
                return sysfault(u"""Nie można nadać czytelnikowi unikatowego numeru
                                  czterocyfrowego. Wszystkie numery są już zajęte. Problem
                                  ten wynika z specyfikacji tejże bazy danych i można 
                                  go tylko naprawić kasując istniejących czytelników""")
            form.save()
            messages.add_message(request, messages.INFO, u'Dodano czytelnika')
            return redirect('/reader/%s/' % form.instance.number)

    return render_to_response('readers/add.html', {'request': request,
                                                     'form': form})

def edit_reader(request, number):
    """Kontroler edycji czytelnika"""
    instance = get_object_or_404(Reader, number=Decimal(number))
    form = ReaderForm(instance=instance)

    if request.method == 'POST':
        form = ReaderForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, u'Zmieniono czytelnika')
            return redirect('/reader/%s/' % form.instance.number)

    return render_to_response('readers/edit.html', {'request': request,
                                                   'form': form,
                                                   'reader': instance})

def delete_reader(request, number):
    """Kontroler kasowania czytelnika"""
    get_object_or_404(Reader, number=Decimal(number)).delete()
    messages.add_message(request, messages.INFO, u'Usunięto czytelnika')
    return redirect('/')