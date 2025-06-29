from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from blog.models import blogsite_post , comments


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
    context = {
        'user': user,
        'posts': posts,
        'title': f"{user.username}'s Profile",
        'posts_count': posts_count,

    }
    return render(request, 'accounts/profile.html', context)