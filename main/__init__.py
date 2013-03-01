from django.shortcuts import render_to_response

def sysfault(message):
    return render_to_response('sysfault.html', {'message': message})