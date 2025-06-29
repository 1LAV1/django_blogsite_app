from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse as httpResponse
from .models import blogsite_post , comments
from .forms import comment_form, blog_form
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# ------------------------------------------------------------------------------------------------------------------
 # Specify the fields to include in the form
# ------------------------------------------------------------------------------------------------------------------

def home(request):
    query= request.GET.get('q')
    if query:
        posts = blogsite_post.objects.filter( Q(title__icontains=query) | Q(content__icontains=query)).order_by('-date_created')
    else:   
        posts= blogsite_post.objects.all().order_by('-date_created')  # Fetch all posts ordered by date_created in descending order

    # posts= blogsite_post.objects.all().order_by('-date_created')  # Fetch all posts ordered by date_created in descending order
    context={
        "posts":posts,
        "query": query,
    }
    return render(request, 'blog/home.html',context)
# ------------------------------------------------------------------------------------------------------------------
def about_view(request):
    return  render(request, 'blog/about.html')
# ------------------------------------------------------------------------------------------------------------------
def post_detail_view(request, post_id):
    post = get_object_or_404(blogsite_post, id=post_id)
    all_comments = post.comments.all().order_by('-date_created')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if user is not authenticated
        form = comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # Make sure your Comment model has an 'author' field
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = comment_form()

    context = {
        'post': post,
        'comments': all_comments,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context)
# ------------------------------------------------------------------------------------------------------------------

@login_required
def create_post_view(request):
    
    if request.method=='POST':
        form=blog_form(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect(home)
    else:   
        form=blog_form()
    context={
        'form': form,
    }
    return render(request, 'blog/create_post.html',context)

# ------------------------------------------------------------------------------------------------------------------

@never_cache
@login_required
def post_update_view(request,post_id):
    post= blogsite_post.objects.get(id=post_id)
    if(post.author != request.user):
        return HttpResponseForbidden("You are not allowed to edit this post.")
    if request.method=='POST':
        form=blog_form(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect(post_detail_view, post_id=post.id)
    else:
        form=blog_form(instance=post)   
    context={
        'form': form,   
        'post': post,
    }
    return render(request,'blog/post_update.html',context)
# ------------------------------------------------------------------------------------------------------------------
@login_required
def post_delete_view(request,post_id):
    if(not request.user.is_authenticated):
        return HttpResponseForbidden("You are not allowed to delete this post.")
    post = blogsite_post.objects.get(id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect(home)
    context = {
        'post': post,
    }
    return render(request, 'blog/post_delete.html', context)




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