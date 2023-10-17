from django.contrib import admin
# Tâm An
from .models import Post, Comment,Categori
# from blog.models import UserProfileInfo

# Tâm An


# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'password', 'fullname','avatar','Interaction_score','role' )
#     search_fields = ['Fullname', 'Create_at', 'Updated_at','Role']
# admin.site.register (UserAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'comments', 'likes_count']
    search_fields = ['title', 'content', 'status']
    
    def author(self, obj):
        return obj.author
        
    def category(self, obj):
        return obj.categori.name 
    
    def likes_count(self, obj):
        return obj.total_likes()

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['Title', "User", 'content', "created_at"]
    search_fields = ["Title", "User", "content"]
    def Title(self, obj):
        return obj.post.title
    def User(self, obj):
        return obj.user
admin.site.register(Comment,CommentAdmin)


class CateAdmin(admin.ModelAdmin):
    list_display = ['name', "Category_Parent"]
    search_fields = ['name','Category_Parent']
    def Category_Parent(self, obj):
        if obj.parent:
            return obj.parent.name
        else:
            return "Root"
admin.site.register(Categori, CateAdmin)


