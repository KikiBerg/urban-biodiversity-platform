from django.contrib import admin
from .models import Category, Post, Comment


class CategoryAdmin(admin.ModelAdmin):
    pass
# the class will be customized shortly

class PostAdmin(admin.ModelAdmin):
    pass
# the class will be customized shortly

class CommentAdmin(admin.ModelAdmin):
    pass
# the class will be customized shortly




# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)