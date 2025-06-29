from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from blog.models import blogsite_post , comments
from .models import userProfile
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


# Create your views here.




def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        email=request.POST['email']

        user=authenticate(username=username,password=password,email=email)
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid username or password")
            return redirect('login')
        
    context={
        "title": "Login",   

    }
    return render(request, 'accounts/login.html', context)




def signup_view(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request,"username already exists")
        else:
            user=User.objects.create_user(username=username, password=password, email=email)
            login(request,user)
            return redirect( 'home' )

    context={
        "title": "Sign Up",   

    }
    return render(request, 'accounts/signup.html', context)



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.") 
    context={
        "title": "Logout",   
    }
    return redirect('home')




def profile_view(request, username):
    user = User.objects.get(username=username)
    posts = blogsite_post.objects.filter(author=user)  # Only posts by this user
    posts_count=posts.count()
    try:
        profile = user.profile
    except userProfile.DoesNotExist:
        profile = None
    context = {
        'user': user,
        'posts': posts,
        'title': f"{user.username}'s Profile",
        'posts_count': posts_count,
        'profile': profile,

    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    profile=request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
  
    return render(request, 'accounts/edit_profile.html', {'form': form})    




@login_required
def like_post_view(request,post_id):
    post=get_object_or_404(blogsite_post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        messages.success(request, "You unliked the post.")
    else:
        post.likes.add(request.user)
        messages.success(request, "You liked the post.")
    return redirect('post_detail', post_id=post.id)
