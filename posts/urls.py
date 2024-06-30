from . import views
from django.urls import path

urlpatterns = [
    # Post URLs
    path('', views.PostListView.as_view(), name='index'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('vote/<int:post_id>/', views.vote_post, name='vote_post'),
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    #path('categories/<str:category_name>/', views.CategoryPostListView.as_view(), name='category_post_list'),
    path('categories/<int:pk>/posts/', views.CategoryPostListView.as_view(), name='category_post_list'),
    # Comment URLs
    path('posts/<int:post_id>/comment/new/', views.CommentCreateView.as_view(), name='comment_create'),
    #path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('post/<slug:slug>/comment/<int:comment_id>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),    
    #path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('post/<slug:slug>/comment/<int:comment_id>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

]