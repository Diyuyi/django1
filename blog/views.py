# Importing necessary libraries and modules
from typing import Any
from django import http
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CommentForm, PostForm
from django.views import generic
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

from django.views.generic.edit import CreateView,DeleteView,UpdateView
from blog.forms import UserForm,UserProfileForm


from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#import for email
from django.core.mail import send_mail
from django.conf import settings

# View to display a list of all posts
# @staff_member_required
# Tâm An
def post_list(request):
    posts = Post.objects.filter(updated_at__isnull=False, status = "0").order_by('-updated_at')
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        post.updated_at = timezone.now()
        post.save()
        return redirect('post_list')
    # Tâm An, sửa lỗi
    # for post in posts:
    #     post.thumbnail = str(post.thumbnail).split('/')[-1]
    return render(request, 'post_list.html', {'posts': posts})
# def post_list(request):
#     posts = Post.objects.filter(updated_at__isnull=False).order_by('-updated_at')
#     if request.method == "POST":
#         post_id = request.POST.get('post_id')
#         post = get_object_or_404(Post, pk=post_id)
#         post.updated_at = timezone.now()
#         post.save()
#         return redirect('post_list')
#     return render(request, 'post_list.html', {'posts': posts})


# Tâm An
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.all().filter(post = pk)
    # if request.method == "POST":
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.post = post
    #         comment.author = request.user
    #         comment.save()
    # else:
    form = CommentForm()
   
    post.thumbnail = str(post.thumbnail).split('/')[-1]
        
    return render(request, 'post_detail.html', {'post': post, 'form': form, 'comments': comments})

# # View to display the details of a specific post
# def post_detail(request, pk):
#     # Query to get a specific post based on its primary key (pk)
#     post = get_object_or_404(Post, pk=pk)
#     # Query to get all comments associated with this post
#     # comments = post.comment_set.all()
#     # Checking if the request method is POST to process the form data
#     if request.method == "POST":
#         form = CommentForm(request.POST)  # Creating a form instance with the submitted data
#         if form.is_valid():  # Validating the form data
#             comment = form.save(commit=False)  # Saving the form data as a comment object, but not saving to the database yet
#             comment.post = post  # Assigning the post to the comment
#             comment.author = request.user  # Assigning the logged in user as the author of the comment
#             comment.save()  # Saving the comment object to the database
#     else:
#         form = CommentForm()  # Creating an empty form instance if the request method is not POST
#     # Rendering the template post_detail.html with the post, comments, and form data
#     return render(request, 'post_detail.html', {'post': post, 'form': form})

# View to add a comment on a specific post

def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=post.id)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # user = User.objects.get(id = request.user)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)  # Redirecting back to the post detail page
    else:
        print(form.errors)
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})

# Additional views for superusers to create, edit, publish posts, and manage drafts
@staff_member_required  # Decorator to ensure only staff members (including superusers) can access this view
def create_post(request):
    # Checking if the request method is POST to process the form data
    if request.method == "POST":
        form = PostForm(request.POST)  # Creating a form instance with the submitted data
        if form.is_valid():  # Validating the form data
            post = form.save(commit=False)  # Saving the form data as a post object, but not saving to the database yet
            post.author = request.user  # Assigning the logged in user as the author of the post
            post.save()  # Saving the post object to the database
            return redirect('post_detail', pk=post.pk)  # Redirecting to the post detail page after successful post creation
    else:
        form = PostForm()  # Creating an empty form instance if the request method is not POST
    # Rendering the template create_edit_post.html with the form data
    return render(request, 'create_edit_post.html', {'form': form})

@staff_member_required  # Decorator to ensure only staff members (including superusers) can access this view
def edit_post(request, pk):
    # Query to get a specific post based on its primary key (pk)
    post = get_object_or_404(Post, pk=pk)
    # Checking if the request method is POST to process the form data
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)  # Creating a form instance with the submitted data and the post instance
        if form.is_valid():  # Validating the form data
            form.save()  # Saving the form data to the database
            return redirect('post_detail', pk=post.pk)  # Redirecting to the post detail page after successful post editing
    else:
        form = PostForm(instance=post)  # Creating a form instance with the post instance if the request method is not POST
    # Rendering the template create_edit_post.html with the form data
    return render(request, 'create_edit_post.html', {'form': form})

@staff_member_required  # Decorator to ensure only staff memberfs (including superusers) can access this view
def publish_post(request, pk):
    # Query to get a specific post based on its primary key (pk)
    post = get_object_or_404(Post, pk=pk)
    post.publish()  # Publishing the post using the publish method defined in the Post model
    return redirect('post_detail', pk=post.pk)  # Redirecting to the post detail page after successful post publishing

@staff_member_required  # Decorator to ensure only staff members (including superusers) can access this view
# Tâm An
def draft_list(request):
    # Query to get all draft posts from the database, ordered by creation date in descending order
    drafts = Post.objects.filter(updated_at__isnull=False, status = "1").order_by('-updated_at')
    # Rendering the template draft_list.html with the drafts data
    print(drafts)
    # for post in drafts:
    #     post.thumbnail = str(post.thumbnail).split('/')[-1]
    return render(request, 'draft_list.html', {'drafts': drafts})
# def draft_list(request):
#     # Query to get all draft posts from the database, ordered by creation date in descending order
#     drafts = Post.objects.filter(updated_at__isnull=True, status=1)
#     # Rendering the template draft_list.html with the drafts data
#     return render(request, 'draft_list.html', {'drafts': drafts})



@staff_member_required
def publish_post_page(request):
    drafts = Post.objects.filter(updated_at__isnull=True)
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        post.updated_at = timezone.now()
        post.save()
        return redirect('publish_post_page')
    return render(request, 'publish_post_page.html', {'drafts': drafts})


# login
def index(request):
    return render(request, 'post_list.html')


#trang logout
def index1(request):
    return render(request, 'post_list.html')
@login_required
def special(request):
    return HttpResponse("You are Logged in!")

@login_required
def special(request):
    return HttpResponse('You are Logged in')

# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('post_list'))
@login_required
def user_logout(request):
    logout(request)
    return redirect('post_list')
    
def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'registration.html',{'user_form': user_form,'profile_form': profile_form   } )
# Tâm An
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # user = User.login(username, password)
        user = authenticate(username = username,password = password)

        if user:
            login(request, user)
            posts = Post.objects.filter(updated_at__isnull=False, status = "0").order_by('-updated_at')
            # for i in posts:
            #    i.thumbnail = str(i.thumbnail).split('/')[-1] 
            return redirect('post_list')
        else:
            return redirect('user_login')
    else:
        return render(request,'login.html',{})
# def user_login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = User.login( username,password )
        

#         if user:
#             if user.is_active:
#                 login(request,user)
#                 return HttpResponseRedirect(reverse('post_list'))
#             else:
#                 return HttpResponse('ACCOUNT NOT ACTIVE')
#         else:
#             print('soneone tried to login anh fail:')
#             print("username: {} and password: {}".format(username,password))
#             return HttpResponse("Đăng nhập thất cmn bại")
#     else:
#         return render(request,'login.html',{})
    # Tâm An
def getAllCommentsForPost(request):
    # Post_ID
    post_id = request.POST.get('post_id')
    comments = Comment.objects.filter(post_id = post_id)
    return render(request, 'post_detail.html', {'comments': comments})

class CreateNewPost(CreateView):
    model = Post
    template_name = "new_post.html"
    fields = ['title','content','categori','status']
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        obj = form.save(commit = False)
        obj.author = User.objects.get(id=self.request.user.id)
        obj.created_at = timezone.now()
        obj.thumbnail = '4572202_cover_home_air_force_one.jpg'
        obj.updated_at = timezone.now()
        obj.comments = 0
        obj.views = 0
        obj.thumbnail = '8107828_CV.jpg'
        obj.save()
        return super().form_valid(form)

class UpdatePost(UpdateView):
    model = Post
    template_name = "update_post.html"
    fields = ['title','content','categori','status']
    success_url = "/"

class DeletePost(DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = "/"
    def tes_func(self):
        post= self.get_object()
        if self.request.user == post.author:
            return True
        return False

# Duy: Public post
@staff_member_required  # Decorator to ensure only staff memberfs (including superusers) can access this view
def publish_post(request, pk):
    # Query to get a specific post based on its primary key (pk)
    post = get_object_or_404(Post, pk=pk)
    post.publish()  # Publishing the post using the publish method defined in the Post model
    # Tâm AN: Muốn return về index
    return redirect('post_list')  # Redirecting to the post detail page after successful post publishing

# An: Like post
# def like_post(request):
#     user = request.user
#     if request.method == 'POST':
#         post_id = request.POST.get('post_id')
#         post_obj = Post.objects.get(id=post_id)
        
#         if user in post_obj.like.all():
#             post_obj.like.remove(user)
#         else:
#             post_obj.like.add(user)
#     return redirect('post_detail')

   

# An: Search
def search_post(request):
    # print(request.POST)
    search_data = request.POST.get('search_title')
    qd = Post.objects.filter(status='0', title__contains = search_data)
    # for post in qd:
    #     post.thumbnail = str(post.thumbnail).split('/')[-1]
    return render(request, 'search.html',{'posts': qd, 'search_title': search_data})

# Duy: Edit comments
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if not comment.can_edit(request.user):
        return HttpResponseForbidden()
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form})

def send_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Gửi email
        send_mail(
            'Chào bạn, cảm ơn đã liên hệ với Django.tdc',
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )

        print("Thanks")
        return redirect('post_list')

    return redirect('post_list')