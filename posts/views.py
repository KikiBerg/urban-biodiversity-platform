from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm

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
    