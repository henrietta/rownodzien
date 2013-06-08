# coding=UTF-8
from rownodzien.main import render_to_response

def main(request):
    """Kontroler strony głównej"""
    return render_to_response('main/main.html', request)



from django import forms
from rownodzien.people.models import Librarian
from django.shortcuts import redirect

class LoginForm(forms.Form):
    """Formularz służący do rejestracji wypożyczenia"""
    id = forms.CharField()
    pesel = forms.CharField()

    def clean(self):
        """Sprawdz istnienie ID-u, PESEL-u i korelacje"""
        data = super(LoginForm, self).clean()

        try:
            id = int(data['id'])
            pesel = int(data['pesel'])
        except:
            raise forms.ValidationError(u'Błędne dane')

        try:
            lbr = Librarian.objects.filter(id=id).get(pesel=pesel)
        except Librarian.DoesNotExist:
            raise forms.ValidationError(u'Błędne dane')

        return data  # Pozwol sie zalogowac

def login(request):
    """Kontroler logowania się"""

    if request.method == 'POST':
        lf = LoginForm(request.POST)
        if lf.is_valid():
            request.session['librarian_id'] = int(lf.cleaned_data['id'])

            return redirect('/')
    else:
        lf = LoginForm()

    return render_to_response('main/login.html', request, form=lf)


def logout(request):
    """Kontroler wylogowania się"""
    del request.session['librarian_id']
    return redirect('/')