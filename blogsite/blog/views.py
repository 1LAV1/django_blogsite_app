from django.shortcuts import render
from django.http import HttpResponse as httpResponse

# Create your views here.
def home(request):
    return httpResponse("Hello, world! LAV learnign django here")

def about_view(request):
    return  render(request, 'blog/about.html')