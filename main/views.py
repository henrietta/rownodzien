# coding=UTF-8
from rownodzien.main import render_to_response

def main(request):
    """Kontroler strony głównej"""
    return render_to_response('main/main.html', request)