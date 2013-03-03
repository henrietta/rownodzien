# coding=UTF-8
from django.shortcuts import render_to_response as djr
from django.template import RequestContext

def sysfault(message):
    return djr('sysfault.html', {'message': message})

def render_to_response(path, request, **kwargs):
    """Drop-in handler dla renderowania
    szablonów. Automatycznie przekazuje szablonowi
    potrzebne dane"""
    kwargs.update({'request': request})
    return djr(path, kwargs, context_instance=RequestContext(request))