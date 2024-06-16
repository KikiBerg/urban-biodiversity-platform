from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
#from django.http import HttpResponse

# Create your views here.
class PostListView(generic.ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-created_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'detail'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs.get('slug'))


class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'slug', 'author', 'featured_image', 'content', 'status', 'excerpt', 'category']


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'slug', 'author', 'featured_image', 'content', 'status', 'excerpt', 'category']


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = '/'


class CategoryListView(ListView):
    model = Category
    template_name = 'posts/category_list.html'   
    context_object_name = 'categories'


class CategoryPostListView(ListView):
    model = Post
    template_name = 'posts/category_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category_name'])
        return Post.objects.filter(category=self.category)


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comment_form.html'
    success_url = reverse_lazy('index')
    fields = ['post', 'author', 'content', 'status']


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comment_form.html'
    success_url = reverse_lazy('index')
    fields = ['content', 'status']


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'posts/comment_confirm_delete.html'
    success_url = reverse_lazy('index')
    