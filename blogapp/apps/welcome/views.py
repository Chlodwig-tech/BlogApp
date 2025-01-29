from django.shortcuts import render

# Create your views here.
def welcome_view(request, *args, **kwargs):  
    return render(request, 'index.html', {})