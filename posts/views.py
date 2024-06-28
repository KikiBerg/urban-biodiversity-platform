from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.http import HttpResponseRedirect

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
    permission_required = 'posts.can_manage_categories'


    def get_context_data(self, **kwargs):
        """
        Adds additional context variables to the template context
        """
        context = super().get_context_data(**kwargs)
        #context['can_manage_categories'] = self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)
        #context['can_manage_categories'] = self.request.user.has_perm('posts.can_manage_categories')
        context['can_manage_categories'] = self.request.user.is_authenticated and self.request.user.has_perm('posts.can_manage_categories')
        
        #print(f' is authenticated: {self.request.user.is_authenticated}')
        #print(f"can manage categories: {self.request.user.has_perm('posts.can_manage_categories')}")

        return context


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

        #self.category = get_object_or_404(Category, name=self.kwargs['category_name'])
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
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
    success_url = reverse_lazy('category_list')
    form_class = CategoryForm
    permission_required = 'posts.can_manage_categories'


    def form_valid(self, form):
        """
        Displays a success message indicating that the category was created successfully,
        then calls the parent class's form_valid method to proceed with the creation process.
        """
        form.instance.created_by = self.request.user
        form.instance.status = 'pending'
        messages.success(self.request, 'Category created successfully! It is pending approval.')
        return super().form_valid(form)


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows users to update the details of a category.
    """
    model = Category
    template_name = 'posts/category_form.html'    
    success_url = reverse_lazy('category_list')
    form_class = CategoryForm
    permission_required = 'posts.can_manage_categories'


    def test_func(self):
        """
        Checks if the current user has staff or superuser privileges
        """
        return self.request.user.has_perm('posts.can_manage_categories') or self.get_object().created_by == self.request.user


    def form_valid(self, form):
        """
        Displays a success message indicating that the 
        category was updated successfully, then calls the parent class's 
        form_valid method to proceed with the update process.
        """
        if not self.request.user.has_perm('posts.can_manage_categories'):
            form.instance.status = 'pending'
            messages.success(self.request, 'Category updated successfully! Changes are pending approval.')
        else:
            messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Handles the deletion of a category.
    """
    model = Category
    template_name = 'posts/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    permission_required = 'posts.can_manage_categories'


    def test_func(self):
        """
        Checks if the current user has staff or superuser privileges to delete a category.
        """
        return self.request.user.has_perm('posts.can_manage_categories') or self.get_object().created_by == self.request.user
        #return self.request.user.is_staff or self.request.user.is_superuser


    def delete(self, request, *args, **kwargs):
        """
        Overrides the default delete method to display a success message after deletion.
        Then it calls the superclass's delete method to proceed with the actuall deletion process.
        """
        if not self.request.user.has_perm('posts.can_manage_categories'):
            messages.success(self.request, 'Category deletion request submitted. It is pending approval.')
            self.object = self.get_object()
            self.object.status = 'pending'
            self.object.save()
            return redirect(self.success_url)
        messages.success(self.request, 'Category deleted successfully!')
        return super().delete(request, *args, **kwargs)


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
    Handles updating/editing existing comments
    """
    model = Comment    
    template_name = 'posts/comment_form.html'
    success_url = reverse_lazy('index')
    #fields = ['content', 'status']
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def get_object(self, queryset=None):
        """
        Retrieves the comment instance based on the 'comment_id' passed in the URL.
        Returns the comment object if found, otherwise raises a Http404 exception.
        """
        comment_id = self.kwargs.get('comment_id')        
        return get_object_or_404(Comment, pk=comment_id)


    def get_success_url(self):
        """
        Generates the URL to redirect to post detail page of 
        the post associated with the commentupon successful form submission.      
        """
        return reverse('post_detail', args=[self.kwargs['slug']])


    def form_valid(self, form):
        """
        Called when the form is valid.
        Saves the updated comment if the current user is the author,
        sets the approved status to False,
        and redirects to the success URL.
        Displays a success message if the update is successful.
        """
        if self.object.author == self.request.user:
            self.object = form.save(commit=False)
            self.object.approved = False
            self.object.save()
            messages.success(self.request, 'Comment Updated!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Error updating comment!')
            return self.form_invalid(form)


    def form_invalid(self, form):
        """
        Called when the form is invalid. 
        Redirects to the form page with error messages.
        """
        messages.error(self.request, 'Error updating comment!')
        return HttpResponseRedirect(self.get_success_url())


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        context['post'] = post
        return context


class CommentDeleteView(DeleteView):
    """
    Handles deleting comments
    """
    model = Comment
    template_name = 'posts/comment_confirm_delete.html'
    success_url = reverse_lazy('index')


    def get_object(self, queryset=None):
        """
        Retrieves the comment to be deleted
        """
        comment_id = self.kwargs.get('comment_id')
        self.comment = get_object_or_404(Comment, pk=comment_id)
        self.post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        return self.comment


    def get_context_data(self, **kwargs):
        """
        Adds additional context data to be used in the template
        """
        context = super().get_context_data(**kwargs)
        context['post'] = self.post
        return context


    def delete(self, request, *args, **kwargs):
        """
        Handles the deletion of the comment
        """
        self.object = self.get_object()
        if self.object.author == request.user:
            success_url = self.get_success_url()
            self.object.delete()
            messages.success(request, 'Comment deleted!')
            return HttpResponseRedirect(success_url)
        else:
            messages.error(request, 'You can only delete your own comments!')
            return HttpResponseRedirect(self.get_success_url())





