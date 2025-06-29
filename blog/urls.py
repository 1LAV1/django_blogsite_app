from . import views
from django.urls import path    
from django.http import HttpResponse




urlpatterns = [
    path('', views.home, name='home'),   
    path('about/',views.about_view,name='about'), 
    path('post/<int:post_id>/',views.post_detail_view,name='post_detail'),
    path('create_post/',views.create_post_view,name='create_post'),
    path('post/<int:post_id>/update/', views.post_update_view, name='post_update'),
    path('post/<int:post_id>/delete/', views.post_delete_view, name='post_delete'),
    path('post/<int:post_id>/like/', views.like_post_view, name='like_post'),
]