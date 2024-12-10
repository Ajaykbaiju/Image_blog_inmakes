from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.admin_login, name='admin_login'),
    
    path('users/', views.manage_users, name='manage_users'),
    path('posts/', views.manage_posts, name='manage_posts'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('block_post/<int:post_id>/', views.block_post, name='block_post'),
    
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    # path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
]
