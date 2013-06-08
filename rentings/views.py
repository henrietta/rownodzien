# coding=UTF-8
"""Moduł z kontrolerami do rejestracji wypożyczenia i zwrotu"""

from django.shortcuts import redirect, get_object_or_404
from django import forms
from django.contrib import messages
from urllib import quote_plus as urlquote
from datetime import datetime, timedelta

from rownodzien.main import render_to_response, sysfault
from rownodzien.books.models import BookInstance
from rownodzien.rentings.models import BookRent

STANDARD_RENTING_TIME = timedelta(14)   # standardowo 14 dni na oddanie

class BookRentForm(forms.ModelForm):
    """Formularz służący do rejestracji wypożyczenia"""
    class Meta:
        model = BookRent
        exclude = ('bookinstance', 'real_due')

class BookReturnForm(forms.Form):
    """Formularz służący do zwrotu książki"""
    when_returned = forms.DateTimeField(initial=datetime.now, label=u'Kiedy oddano')
    was_damaged = forms.BooleanField(required=False, label=u'Czy uszkodzona?')
    was_lost = forms.BooleanField(required=False, label=u'Czy zagubiona?')

def register_return(request, code):
    """Kontroler zwrotu książki"""
    bookinstance = get_object_or_404(BookInstance, code=code)

    if not bookinstance.is_rented():
        return sysfault(u'Ten egzemplarz nie wypożyczony, tak więc nie można go oddać!')

    form = BookReturnForm()
    if request.method == 'POST':
        form = BookReturnForm(request.POST)
        if form.is_valid():
            bookinstance.get_renting().close(was_damaged=form.cleaned_data['was_damaged'],
                                             was_lost=form.cleaned_data['was_lost'])
            # Teraz przekieruj na stronę egzemplarza
            messages.add_message(request, messages.INFO, u'Zarejestrowano zwrot egzemplarza')
            return redirect(bookinstance.get_absolute_url())

    return render_to_response('rentings/return.html', request,
                                bookinstance=bookinstance,
                                bookrent=bookinstance.get_renting(),
                                form=form)

def register_rent(request, code):
    """Kontroler wypożyczenia książki"""
    bookinstance = get_object_or_404(BookInstance, code=code)

    if bookinstance.is_rented():
        return sysfault(u'Ten egzemplarz jest już wypożyczony i nie można go wypożyczyć ponownie!')

    form = BookRentForm(initial={'official_due': datetime.now()+STANDARD_RENTING_TIME,
                                 'who': request.librarian})
    if request.method == 'POST':
        form = BookRentForm(request.POST)
        if form.is_valid():
            form.instance.bookinstance = bookinstance
            form.save()
            messages.add_message(request, messages.INFO, u'Zarejestrowano wypożyczenie egzemplarza')
            # Teraz przekieruj na stronę egzemplarza
            return redirect(bookinstance.get_absolute_url())

    return render_to_response('rentings/renting.html', request,
                                bookinstance=bookinstance,
                                form=form)
 
