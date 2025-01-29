from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    ProfileView,
    MyProfileView,
)

urlpatterns = [
    path('myprofile/', MyProfileView.as_view(), name='my_profile'),
    path('<slug:slug>/', ProfileView.as_view(), name='profiles'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)