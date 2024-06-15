from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostListView.as_view(), name='posts_list'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]