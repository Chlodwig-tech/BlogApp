from django.shortcuts import redirect

def when_logged_inc(func):
    def inside_function(obj, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')

        return func(obj, request, *args, **kwargs)
    return inside_function

def when_logged_outc(func):
    def inside_function(obj, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/welcome')

        return func(obj, request, *args, **kwargs)
    return inside_function

def when_logged_in(func):
    def inside_function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')

        return func(request, *args, **kwargs)
    return inside_function

def when_logged_out(func):
    def inside_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/welcome')

        return func(request, *args, **kwargs)
    return inside_function