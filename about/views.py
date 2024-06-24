from django.contrib import messages
from django.shortcuts import render
from .models import About, ContactUs
from .forms import ContactUsForm

# Create your views here.
def about_contact(request):
    """
    Renders the About/Contact page
    """
    about = About.objects.all().order_by('-updated_at').first()
    contact_us_form = ContactUsForm

    return render(
        request,
        "about/about.html",
        {"about": about,
        "contact_us_form": contact_us_form
        },
    )



    