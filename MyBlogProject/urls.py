"""
URL configuration for MyBlogProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from django.conf import settings
from blog import views
from django.conf.urls.static import static


urlpatterns = [
    # path('', views.post_list,name="post_list"),
    # path('', admin.site.urls),
    # path('', include('blog.urls')),
    # path('', views.post_list, name='post_list'),
    # re_path(r'^special/',views.special,name='special'),


    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    re_path(r'^logout/',views.user_logout,name='logout'),
    path('', views.post_list, name='post_list'),
    re_path(r'^special/',views.special,name='special'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
