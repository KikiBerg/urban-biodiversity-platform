from django import forms
from .models import Post, Comment, Category
from .constants import STATUS_CATEGORIES


class PostForm(forms.ModelForm):
    """
    Form for creating or editing posts, including title, slug, author, 
    featured image, content, status, excerpt, and category.    
    """
    class Meta:
        model = Post
        fields = ['title', 'slug', 'author', 'featured_image', 'content', 'status', 'excerpt', 'category']


class CommentForm(forms.ModelForm):
    """
    Form for adding or editing comments on posts, including post reference, 
    author, content, and status.   
    """
    class Meta:
        model = Comment        
        fields = ['content']


class CategoryForm(forms.ModelForm):
    """
    Form for managing categories, including name and description.    
    """
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


    def clean_name(self):
        """
        Method to ensure the category name is unique across all instances,
        excluding the current instance being edited.    
        """
        name = self.cleaned_data['name']
        if Category.objects.filter (name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A category with this name already exists.')
        return name


    def __init__(self, *args, **kwargs):
        """
        Method to exclude the status field for non-admin users
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.has_perm('posts.can_manage_categories'):
            self.fields['status'] = forms.ChoiceField(choices=STATUS_CATEGORIES)