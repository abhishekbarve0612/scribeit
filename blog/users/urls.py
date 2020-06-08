from django.contrib import admin
from django.urls import path
from . import views


app_name = 'users'


urlpatterns = [
    path('register/', views.register,name='register' ),
    path('user_login/', views.user_login,name='user_login' ),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'), 
    path('managePosts/', views.managePosts, name='manage-posts'),
    path('logout/', views.logmeout, name='log-out'),
    path('beblogger/', views.makeBloggers, name='make-bloggers'),
    path('profile/', views.userProfile, name='user-profile'),
    path('profile-edit/', views.edit_profile, name='user-profile-edit'),
    path('', views.adminHome, name='admin-home'),
    
]
