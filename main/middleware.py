from django.shortcuts import redirect
from rownodzien.people.models import Librarian
from rownodzien.main.views import login

class LibrarianLoginMiddleware(object):
    def process_view(self, request, view_func, *args, **kwargs):
        """Funkcja wywolywana tuz przed tym jak Django zamierza wywolac
        kontroler"""
        if view_func == login:
            return None         # Logowac sie mozna zawsze

        try:            # W sesji musi byc odpowiedni integer z ID
                        # bibliotekarza zeby to mialo sens
            sid = int(request.session['librarian_id'])
        except (ValueError, KeyError):
            return redirect('/login/')

        try:            # Ten bibliotekarz musi tez istniec
            lbr = Librarian.objects.get(id=sid)
        except Librarian.DoesNotExist:
            return redirect('/login/')

        request.librarian = lbr # Zachowaj dla wywolan

        return None # Zezwol na logowanie
