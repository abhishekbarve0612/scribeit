from django.contrib import admin
from django.urls import path

from . import views
# from .views import editBlog


urlpatterns = [
    #path('', views.classListView.as_view()),
    path('', views.home, name = "posts-home" ),
    # path('login/', views.register, name = "login" ),
    path('posts/', views.enlist_post, name = "post-list" ),
    path('404/', views.handler404, name = "post-404" ),
    path('500/', views.handler500, name = "post-500" ),
    path('create/', views.create_post, name = "create-post" ),
    path('contact/', views.contactAdmin, name = "contact-admin" ),
    path('about/', views.aboutUs, name = "about-us" ),
    path('like/<int:id>/', views.like, name = "post-like" ),
    path('view/<slug:slug>', views.view_post, name = "post-detail" ),
    path('delete/<slug:slug>', views.delete_post, name = "delete-post" ),
    path('view/<slug:slug>/edit/', views.update_post, name = "edit-post" ),
    path('blogRequest/<slug:slug>/', views.blogRequest, name = "blog-request" ),
    path('authorProfile/<int:id>/', views.authorProfile, name = "author-profile" ),
    # path('edit2/<int:pk>', views.editBlog.as_view(), name = "edit-post" ),
]
