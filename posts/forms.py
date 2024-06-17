from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'author', 'featured_image', 'content', 'status', 'excerpt', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post', 'author', 'content', 'status']