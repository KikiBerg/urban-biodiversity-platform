from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
#from django.http import HttpResponse

# Create your views here.
class PostListView(ListView):
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


#class PostCreateView(CreateView):
    #pass
# the class will be customized shortly


#class PostUpdateView(UpdateView):
    #pass
# the class will be customized shortly


#class PostDeleteView(DeleteView):
    #pass
# the class will be customized shortly


#class CategoryListView(ListView):
    #pass
# the class will be customized shortly


#class CategoryPostListView(ListView):
    #pass
# the class will be customized shortly


#class CommentCreateView(CreateView):
    #pass
# the class will be customized shortly


#class CommentUpdateView(UpdateView):
    #pass
# the class will be customized shortly


#class CommentDeleteView(DeleteView):
    #pass
# the class will be customized shortly