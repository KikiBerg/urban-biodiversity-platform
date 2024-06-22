from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages


# Import Django's authentication mixins to ensure that users are logged in and have the required permissions
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, CategoryForm

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
        """
        Retrieve the Post object based on the provided slug
        """
        return get_object_or_404(Post, slug=self.kwargs.get('slug'))



    def get_context_data(self, **kwargs):
        """
        Add additional context data for rendering the post detail page
        """
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comment_set.all().order_by('-created_at')
        comment_count = post.comment_set.filter(status='approved').count()
        comment_form = CommentForm()

        # Updating the context dictionary with additional variables
        context.update({
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form
        })
        return context


    def post (self, request, *args, **kwargs):
        """        
        Handles POST requests to submit new comments.
        """
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )
            context['comment_form'] = CommentForm()
        else:
            context['comment_form'] = comment_form
        
        return self.render_to_response(context)


class CategoryListView(ListView):
    """
    Displays a list of all categories available in the blog.
    """
    model = Category
    template_name = 'posts/category_list.html'   
    context_object_name = 'categories'


class CategoryPostListView(ListView):
    """    
    This class-based view inherits from ListView and is used 
    to render a list of blog posts belonging to a particular category. 
    It retrieves the requested category from the URL,filters posts 
    based on that category, and provides them to the template for rendering.
    """
    model = Post
    template_name = 'posts/category_post_list.html'
    context_object_name = 'posts'


    def get_queryset(self):
        """
        Method to retrieve the requested category from the URL and filter the Post objects 
        based on that category.

        - Retrieve the 'category_name' argument from the URL kwargs.
        - Use get_object_or_404 to fetch the Category object with the matching name, 
          raising a 404 error if not found.
        - Filter Post objects based on the retrieved category and returns the filtered queryset.
        """

        self.category = get_object_or_404(Category, name=self.kwargs['category_name'])
        return Post.objects.filter(category=self.category)


    def get_context_data(self, **kwargs):
        """
        Method to add additional context data to be passed to the template.

        - Call the superclass's get_context_data method to get the default context data.
        - Add the 'category' object to the context dictionary, making it accessible in the template.
        - Return the updated context dictionary.
        """
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """
    Creates new categories
    """
    model = Category
    template_name = 'posts/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('category_list')
    categories_form = CategoryForm


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows users to update the details of a category.
    """
    model = Category
    template_name = 'posts/category_form.html'
    fields = ['name', 'description']
    categories_form = CategoryForm    
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handles the deletion of a category.
    """
    model = Category
    template_name = 'posts/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')



class PostCreateView(CreateView):
    """
    Handles the creation of new posts
    """
    model = Post    
    template_name = 'posts/post_form.html'
    fields = ['title', 'slug', 'author', 'featured_image', 'content', 'status', 'excerpt', 'category']
    success_url = reverse_lazy('posts:index')


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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
    