from django.contrib import messages
from django.shortcuts import render
from .models import About, ContactUs
from .forms import ContactUsForm


# Create your views here.
def about_contact(request):
    """
    Renders the most recent information on the website author
    and allows user contact requests
    Displays an individual instance of :model:`about_contact.About`

     **Context**
    ``about_contact``
        The most recent instance of :model:`about_contact.About`.
        ``contact_us_form``
            An instance of :form:`about_contact.ContactUsForm`.

    **Template**
    :template:`about_contact/about.html`
    """
    if request.method == "POST":
        contact_us_form = ContactUsForm(data=request.POST)
        if contact_us_form.is_valid():
            contact_us_form.save(
                messages.add_message(request, messages.SUCCESS,
                                     "Your message has been received! "
                                     "We'll get back to you soon.")
            )

    about = About.objects.all().order_by('-updated_at').first()
    contact_us_form = ContactUsForm

    return render(
        request,
        "about/about.html",
        {"about": about,
         "contact_us_form": contact_us_form
         },
    )
