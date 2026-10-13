

# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post,Like,Comment,Follow,Notification
from django.contrib import messages
from .models import Profile

def home(request):

    if request.method == "POST":

        if not request.user.is_authenticated:
            return redirect('login')

        content = request.POST.get("content")

        if content:
            Post.objects.create(
                user=request.user,
                content=content
            )

        return redirect('home')

    posts = Post.objects.all().order_by('-created_at')

    return render(
        request,
        'social/home.html',
        {'posts': posts}
    )


def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(
                request,
                'social/register.html',
                {'error': 'Passwords do not match'}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'social/register.html',
                {'error': 'Username already exists'}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect('home')

    return render(request, 'social/register.html')


def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(
            request,
            'social/login.html',
            {'error': 'Invalid username or password'}
        )

    return render(request, 'social/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if created and post.user != request.user:
            Notification.objects.create(
                recipient=post.user,
                sender=request.user,
                notification_type='like',
                post=post
            )

        elif not created:
            like.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def add_comment(request, post_id):

    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)

        content = request.POST.get('content', '').strip()

        if content:
            Comment.objects.create(
                user=request.user,
                post=post,
                content=content
            )

    return redirect('home')
@login_required
def profile(request, username):
    profile_user = get_object_or_404(
        User,
        username=username
    )

    profile, created = Profile.objects.get_or_create(
        user=profile_user
    )

    posts = Post.objects.filter(
        user=profile_user
    ).order_by('-created_at')

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    return render(
        request,
        'social/profile.html',
        {
            'profile_user': profile_user,
            'profile': profile,
            'posts': posts,
            'followers_count': followers_count,
            'following_count': following_count,
            'is_following': is_following,
        }
    )


    user_posts = Post.objects.filter(
        user=profile_user
    ).order_by('-created_at')

    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    context = {
        'profile_user': profile_user,
        'user_posts': user_posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }

    return render(
        request,
        'social/profile.html',
        context
    )
@login_required
def follow_user(request, username):
    target_user = get_object_or_404(
        User,
        username=username
    )

    if request.method == 'POST' and target_user != request.user:
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )

        if created:
            Notification.objects.create(
                recipient=target_user,
                sender=request.user,
                notification_type='follow'
            )
        else:
            follow.delete()

    return redirect(
        'profile',
        username=target_user.username
    )
@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        bio = request.POST.get('bio', '').strip()
        picture = request.FILES.get('profile_picture')

        if not username:
            messages.error(request, 'Username cannot be empty.')

        elif User.objects.filter(username=username).exclude(
            pk=request.user.pk
        ).exists():
            messages.error(request, 'This username is already taken.')

        else:
            request.user.username = username
            request.user.save()

            profile.bio = bio

            if picture:
                profile.profile_picture = picture

            profile.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', username=request.user.username)

    return render(
        request,
        'social/edit_profile.html',
        {
            'profile': profile,
        }
    )
@login_required
def notifications(request):
    notification_list = Notification.objects.filter(
        recipient=request.user
    ).select_related(
        'sender',
        'post'
    ).order_by('-created_at')

    notification_list.filter(
        is_read=False
    ).update(is_read=True)

    return render(
        request,
        'social/notifications.html',
        {'notifications': notification_list}
    )
@login_required
def search_users(request):
    query = request.GET.get('q', '').strip()

    if query:
        users = User.objects.filter(
            username__icontains=query
        ).exclude(
            id=request.user.id
        ).order_by('username')[:50]
    else:
        users = User.objects.none()

    return render(
        request,
        'social/search_users.html',
        {
            'users': users,
            'query': query
        }
    )