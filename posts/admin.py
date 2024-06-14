from django.contrib import admin
from .models import Category, Post, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'status', 'category')
    list_filter = ('status', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
   

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('author', 'content')



# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)