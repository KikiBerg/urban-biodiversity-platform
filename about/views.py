from django.shortcuts import render
from .models import About

# Create your views here.
def about_contact(request):
    """
    Renders the About/Contact page
    """
    about = About.objects.all().order_by('-updated_at').first()

    return render(
        request,
        "about/about.html",
        {"about": about},
    )