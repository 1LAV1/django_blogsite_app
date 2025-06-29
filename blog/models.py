from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class blogsite_post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    author=models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model
    date_created=models.DateTimeField(auto_now_add=True)#created that is why auto_now_add
    date_updated=models.DateTimeField(auto_now=True)#updated that is why auto_now

    def __str__(self):
        return self.title








class comments(models.Model):
    post=models.ForeignKey(blogsite_post, on_delete=models.CASCADE, related_name='comments')
    author=models.ForeignKey(User, on_delete=models.CASCADE)    
    content=models.TextField()
    date_created=models.DateTimeField(auto_now_add=True)
    # date_updated=models.DateTimeField(auto_now=True)
    # 
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"  

