from django.shortcuts import render,redirect
from django.http import HttpResponse as httpResponse
from .models import blogsite_post
from django import forms
from django.contrib.auth.decorators import login_required




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