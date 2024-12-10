from django.urls import path
from . import views
from .views import update_profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index', views.index, name='index'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    
    
    path('',views.CustomLoginView.as_view(), name='login'),
   
    path('register/',views.register, name='register'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),


    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/complete/', views.password_reset_complete, name='password_reset_complete'),
    path('password_reset_failed/', views.password_reset_failed, name='password_reset_failed'),
]
