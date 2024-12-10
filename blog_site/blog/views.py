from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import CommentForm

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', '/'))
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('index')  

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)  # Logs the user out
    return redirect('login')  # Redirects to the login page

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, UserProfileForm

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})




from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, UserProfileForm
from .models import UserProfile


@login_required
def profile(request):
    # Ensure user has a profile
    if not hasattr(request.user, 'userprofile'):
        UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'blog/profile.html', {'user_form': user_form, 'profile_form': profile_form})

# from django.contrib.auth.forms import PasswordResetForm
# from django.core.mail import send_mail, BadHeaderError
# from django.contrib.auth.tokens import default_token_generator
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, force_bytes
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.db.models import Q

# def password_reset_request(request):
#     if request.method == 'POST':
#         password_form = PasswordResetForm(request.POST)
#         if password_form.is_valid():
#             # Corrected the syntax for accessing cleaned data
#             data = password_form.cleaned_data.get('email')  # Use parentheses
#             user_email = User.objects.filter(Q(email=data))  # Use `Q()` for complex queries
#             if user_email.exists():
#                 for user in user_email:
#                     # Define email subject and template
#                     subject = 'Password Reset Request'
#                     email_template_name = 'registration/password_message.txt'
#                     parameters = {
#                         'email': user.email,
#                         'domain': '127.0.0.1:8000',
#                         'site_name': 'Blogsite',
#                         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                         'token': default_token_generator.make_token(user),
#                         'protocol': 'http',
#                     }
#                     # Render the email template with context
#                     email = render_to_string(email_template_name, parameters)
#                     try:
#                         # Send email
#                         send_mail(subject, email, '', [user.email], fail_silently=False)
#                     except BadHeaderError:
#                         return HttpResponse('Invalid header found.')
                    
#                     return redirect('password_reset_done')  # Redirect after email is sent

#     else:
#         password_form = PasswordResetForm()

#     context = {
#         'password_form': password_form,
#     }
#     return render(request,'registration/password_reset_1.html', context)
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ensure only the author can edit the post
    if post.author != request.user:
        raise PermissionDenied("You are not authorized to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.id)  # Redirect to post detail
    else:
        form = PostForm(instance=post)  # Pre-fill the form with post data

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, UserProfileForm

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('update_profile')  # Stay on the update profile page
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'profile/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def password_reset_request(request):
    """Handle the password reset request form."""
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            email = password_form.cleaned_data['email']
            users = User.objects.filter(email=email)
            if users.exists():
                for user in users:
                    # Generate token and UID
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    domain = get_current_site(request).domain
                    subject = 'Reset Your Password'
                    email_template_name = 'registration/password_reset_email.txt'
                    parameters = {
                        'email': user.email,
                        'domain': domain,
                        'site_name': 'Your Website',
                        'uid': uid,
                        'token': token,
                        'protocol': 'http',
                    }
                    email_message = render_to_string(email_template_name, parameters)
                    send_mail(subject, email_message, '', [user.email])

                messages.success(request, 'Password reset link has been sent to your email address.')
                return redirect('password_reset_done')

    else:
        password_form = PasswordResetForm()
    
    return render(request, 'registration/password_reset.html', {'password_form': password_form})

def password_reset_done(request):
    """Page displayed after sending password reset email."""
    return render(request, 'registration/password_reset_done12.html')
from django.utils.encoding import force_str

from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str  # Use force_str instead of force_text

def password_reset_confirm(request, uidb64, token):
    try:
        # Decode the UID from the URL-safe base64 encoding
        uid = force_str(urlsafe_base64_decode(uidb64))  # Use force_str instead of force_text
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Token is valid, proceed to password reset
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()  # Save the new password
                return redirect('password_reset_complete')  # Redirect to completion page
        else:
            form = SetPasswordForm(user)  # Empty form to input new password
        
        return render(request, 'registration/password_reset_confirm34.html', {'form': form})
    
    else:
        return redirect('password_reset_failed')  # Redirect to an error page if token is invalid
def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete56.html')

# In your views.py


def password_reset_failed(request):
    return render(request, 'registration/password_reset_failed.html')


