from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Danh mục bài viết
class Categori(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='cate_chill')
    # ...

    def __str__(self):
        parent_id = self.parent_id if self.parent else 'None'
        return f'ID: {self.id:<10} | Name: {self.name:<25} | Parent: {parent_id:<25} |'


# Post bài viết trên web blog
class Post(models.Model):
    title =models.CharField(max_length=255)
    content = models.TextField()
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_post')
    categori  = models.ForeignKey(Categori, on_delete=models.CASCADE, related_name='categori_post') 
    thumbnail = models.ImageField(upload_to='', null=True)
    # thumbnail = models.ImageField(null=True)
    status = models.IntegerField(choices=[(0, 'Public'), (1, 'Pravited')], default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    comments = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    
    def publish(self):
        self.status = 0
        self.save()

    def total_likes(self):
        return self.likes.count()

    def user_liked(self, user):
        return self.likes.filter(id=user.id).exists()

class Comment (models.Model):
    # id = models.AutoField(primary_key=True)
    post  = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    user  = models.ForeignKey(User, on_delete=models.CASCADE , related_name='user_comment')
    content = models.TextField(editable =True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.post.title
    def can_edit(self, user):
        return user.is_staff or user == self.author

    

# Lâm: Login
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    portfolito_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True)

    def __str__(self):
        return self.user.username