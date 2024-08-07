from . import views
from django.urls import path

urlpatterns = [
    # Post URLs
    path('', views.PostListView.as_view(), name='index'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(),
         name='post_detail'),
    path('posts/new/', views.PostCreateView.as_view(),
         name='post_create'),
    path('posts/<slug:slug>/edit/', views.PostUpdateView.as_view(),
         name='post_update'),
    path('posts/<slug:slug>/delete/', views.PostDeleteView.as_view(),
         name='post_delete'),
    # Category URLs
    path('categories/', views.CategoryListView.as_view(),
         name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(),
         name='category_create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(),
         name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(),
         name='category_delete'),
    path('categories/<int:pk>/posts/', views.CategoryPostListView.as_view(),
         name='category_post_list'),
    path('categories/<int:pk>/update_status/', views.update_category_status,
         name='update_category_status'),

    # Comment URLs
    path('posts/<int:post_id>/comment/new/',
         views.CommentCreateView.as_view(), name='comment_create'),
    path('post/<slug:slug>/comment/<int:comment_id>/edit/',
         views.CommentUpdateView.as_view(), name='comment_edit'),
    path('post/<slug:slug>/comment/<int:comment_id>/delete/',
         views.CommentDeleteView.as_view(), name='comment_delete'),
]
