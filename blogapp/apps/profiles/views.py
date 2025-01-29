from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Profile, generate_unique_filename
from .forms import ProfileImageForm
from utilities.authenticators import when_logged_inc

# Create your views here.
class ProfileView(View):

    def get(self, request, slug, *args, **kwargs):        
        user = get_object_or_404(User, username=slug)
        profile = get_object_or_404(Profile, user=user)

        context = {
            'profile' : profile
        }

        return render(request, 'profiles/index.html', context)

class MyProfileView(View):

    @when_logged_inc
    def get(self, request, *args, **kwargs):

        user = request.user
        profile = get_object_or_404(Profile, user=user)
        print(profile.image)
        
        context = {
            'profile' : profile,
            'profileImageForm' : ProfileImageForm(),
        }
        return render(request, 'profiles/detail.html', context)
    
    @when_logged_inc
    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        try:
            print(request.POST, request.FILES)
            if 'bio_data' in request.POST:
                profile.bio = request.POST.get('bio_data')
                profile.save()
                return JsonResponse({'response': profile.bio})
            if 'image' in request.FILES:
                form = ProfileImageForm(request.POST, request.FILES, instance=profile)
                if form.is_valid():
                    form.save()
                else:
                    print('not valid', form.errors)
                return redirect('.')
                
        except Exception as e:
            print('xd', e)