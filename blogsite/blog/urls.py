from . import views
from django.urls import path    
from django.http import HttpResponse




urlpatterns = [
    path('', views.home, name='home'),   
    path('about/',views.about_view,name='about'), 
    path('post/<int:post_id>/',views.post_detail_view,name='post_detail'),
    path('create_post/',views.create_post_view,name='create_post'),
]