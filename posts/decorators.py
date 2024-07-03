from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Category


# Function decorator to ensure that the user is
# either a superuser or the creator of the category
def superuser_or_creator_required(view_func):
    def wrapper(request, *args, **kwargs):
        category_id = kwargs.get('pk')
        category = get_object_or_404(Category, pk=category_id)
        if request.user.is_superuser or category.created_by == request.user:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You don't have permission "
                                    "to edit or delete this category.")
            return redirect('category_list')
    return wrapper


# Function decorator to ensure that the user is a superuser
def superuser_required(view_func):
    decorated_view_func = (user_passes_test
                           (lambda u: u.is_superuser, login_url='login')
                           (view_func)
                           )
    return decorated_view_func
