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

def register_rent(request, code):
    bookinstance = get_object_or_404(BookInstance, code=code)

    if bookinstance.is_rented():
        return sysfault(u'Ten egzemplarz jest już wypożyczony i nie można go wypożyczyć ponownie!')

    form = BookRentForm(initial={'official_due': datetime.now()+STANDARD_RENTING_TIME})
    if request.method == 'POST':
        form = BookRentForm(request.POST)
        if form.is_valid():
            form.instance.bookinstance = bookinstance
            form.save()
            # Teraz przekieruj na stronę egzemplarza
            return redirect('/instance/%s/' % urlquote(bookinstance.code))

    return render_to_response('rentings/renting.html', request,
                                bookinstance=bookinstance,
                                form=form)
 
