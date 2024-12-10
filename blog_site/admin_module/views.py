from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from blog.models import Post
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

# Admin Check Decorator
def admin_only(user):
    return user.is_superuser

@user_passes_test(admin_only)
def admin_dashboard(request):
    user_count = User.objects.count()
    post_count = Post.objects.count()
    return render(request, 'admin_module/dashboard.html', {'user_count': user_count, 'post_count': post_count})



from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

def admin_only(user):
    return user.is_superuser

@user_passes_test(admin_only)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin_module/manage_users.html', {'users': users})

@user_passes_test(admin_only)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, f'User {user.username} has been deleted.')
    return redirect('manage_users')

@user_passes_test(admin_only)
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    status = 'blocked' if not user.is_active else 'unblocked'
    messages.success(request, f'User {user.username} has been {status}.')
    return redirect('manage_users')

@user_passes_test(admin_only)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Post has been deleted.')
    return redirect('manage_posts')

@user_passes_test(admin_only)
def block_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.is_active = not getattr(post, 'is_active', True)
    post.save()
    status = 'blocked' if not getattr(post, 'is_active', True) else 'unblocked'
    messages.success(request, f'Post has been {status}.')
    return redirect('manage_posts')
def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:  # Allow login only for superusers
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Access denied. You are not an admin.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'admin_module/admin_login.html', {'form': form})
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render



@user_passes_test(admin_only)
def manage_posts(request):
    posts = Post.objects.all().order_by('-created_at')  # Fetch all posts, sorted by creation time
    return render(request, 'admin_module/manage_posts.html', {'posts': posts})

