from django.urls import path

from .views import (
    BlogView,
    PostCreateView,
    PostView,
    PostDeleteView,
    PostEditView
)

urlpatterns = [
    path('', BlogView.as_view(), name='posts'),
    path('create/', PostCreateView.as_view(), name='posts-create'),
    path('delete/<slug:slug>/', PostDeleteView.as_view(), name='posts-delete'),
    path('edit/<slug:slug>/', PostEditView.as_view(), name='posts-edit'),
    path('<slug:slug>/', PostView.as_view(), name='posts-detail'),
]