from django.contrib import admin
from .models import Category, Post, Comment
from django_summernote.admin import SummernoteModelAdmin


# Display a table of related posts within the category admin interface
class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ('title', 'author', 'status', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


# Registering the Category model with the Django admin interface
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status',
                    'created_by', 'post_count')
    list_filter = ('status',)
    search_fields = ('name', 'description')
    inlines = [PostInline]

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Number of Posts'


# Registering the Post model with the Django admin interface
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'created_at',
                    'status', 'category')
    list_filter = ('status', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    summernote_fields = ('content',)


# Registering the Comment model with the Django admin interface
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content',
                    'created_at', 'status', 'approved')
    list_filter = ('status', 'created_at', 'approved')
    search_fields = ('author', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected comments "
                                   "have been approved.")
    approve_comments.short_description = "Approve selected comments"
