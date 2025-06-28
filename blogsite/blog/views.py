from django.shortcuts import render,redirect
from django.http import HttpResponse as httpResponse
from .models import blogsite_post
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache



# ------------------------------------------------------------------------------------------------------------------
class blog_form(forms.ModelForm):
    class Meta:
        model= blogsite_post

        fields= ['title','content']  # Specify the fields to include in the form


# ------------------------------------------------------------------------------------------------------------------

def home(request):
    posts= blogsite_post.objects.all().order_by('-date_created')  # Fetch all posts ordered by date_created in descending order
    context={
        "posts":posts,
    }
    return render(request, 'blog/home.html',context)
# ------------------------------------------------------------------------------------------------------------------
def about_view(request):
    return  render(request, 'blog/about.html')
# ------------------------------------------------------------------------------------------------------------------
def post_detail_view(request,post_id):
    try:
        post = blogsite_post.objects.get(id=post_id)
    except blogsite_post.DoesNotExist:
        return httpResponse("Post not found", status=404)

    context = {
        "post": post,
    }
    return render(request, 'blog/post_detail.html', context)
# ------------------------------------------------------------------------------------------------------------------

# @login_required
def create_post_view(request):
    if request.method=='POST':
        form=blog_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(home)
    else:   
        form=blog_form()
    context={
        'form': form,
    }
    return render(request, 'blog/create_post.html',context)

# ------------------------------------------------------------------------------------------------------------------

@never_cache
def post_update_view(request,post_id):
    post= blogsite_post.objects.get(id=post_id)
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
def post_delete_view(request,post_id):
    post = blogsite_post.objects.get(id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect(home)
    context = {
        'post': post,
    }
    return render(request, 'blog/post_delete.html', context)