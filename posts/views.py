from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
#from django.http import HttpResponse

# Create your views here.
class PostListView(ListView):
    pass
# the class will be customized shortly


class PostDetailView(DetailView):
    pass
# the class will be customized shortly


class PostCreateView(CreateView):
    pass
# the class will be customized shortly


class PostUpdateView(UpdateView):
    pass
# the class will be customized shortly


class PostDeleteView(DeleteView):
    pass
# the class will be customized shortly


