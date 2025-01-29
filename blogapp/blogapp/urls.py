"""
URL configuration for blogapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from user_authentication.views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.welcome.urls')),
    path('welcome/', include('apps.welcome.urls')),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView),
    path('blog/', include('apps.blog.urls')),
    path('profiles/', include('apps.profiles.urls')),
    path('ckeditor/', include('django_ckeditor_5.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)