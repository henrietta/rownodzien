# coding=UTF-8
from django.shortcuts import render_to_response

def main(request):
    """Kontroler strony głównej"""
    return render_to_response('main/main.html')