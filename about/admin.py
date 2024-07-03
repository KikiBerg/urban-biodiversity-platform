from django.contrib import admin
from .models import About, ContactUs
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


# Registering the About model with the Django admin interface
@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


# Registering the ContactUs model with the Django admin interface
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('message', 'read',)
