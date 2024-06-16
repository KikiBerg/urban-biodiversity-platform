from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
#from django.http import HttpResponse

# Create your views here.
class PostListView(ListView):
    """
    Displays a list of all blog posts
    """
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-created_at')


class PostDetailView(DetailView):
    """
    Displays the details of a single post
    """
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'detail'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs.get('slug'))


class PostCreateView(CreateView):
    """
    Handles the creation of new posts
    """
    model = Post    
    template_name = 'posts/post_form.html'
    fields = ['title', 'slug', 'author', 'featured_image', 'content', 'status', 'excerpt', 'category']
    success_url = reverse_lazy('posts:index')


class PostUpdateView(UpdateView):
    """
    Handles updating existing posts
    """
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'slug', 'author', 'featured_image', 'content', 'status', 'excerpt', 'category']
    success_url = reverse_lazy('posts:index')


class PostDeleteView(DeleteView):
    """
    Handles deleting posts
    """
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:index')


class CategoryListView(ListView):
    """
    Displays a list of all blog categories
    """
    model = Category
    template_name = 'posts/category_list.html'   
    context_object_name = 'categories'


class CategoryPostListView(ListView):
    """
    Displays a list of blog posts within a specific category
    """
    model = Post
    template_name = 'posts/category_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category_name'])
        return Post.objects.filter(category=self.category)


class CommentCreateView(CreateView):
    """
    Handles the creation of new comments
    """
    model = Comment    
    template_name = 'posts/comment_form.html'
    success_url = reverse_lazy('index')
    fields = ['post', 'author', 'content', 'status']


class CommentUpdateView(UpdateView):
    """
    Handles updating existing comments
    """
    model = Comment    
    template_name = 'posts/comment_form.html'
    success_url = reverse_lazy('index')
    fields = ['content', 'status']


class CommentDeleteView(DeleteView):
    """
    Handles deleting comments
    """
    model = Comment
    template_name = 'posts/comment_confirm_delete.html'
    success_url = reverse_lazy('index')
    