from django.db import models

# Create your models here.
class blogsite_post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date_created=models.DateTimeField(auto_now_add=True)#created that is why auto_now_add
    date_updated=models.DateTimeField(auto_now=True)#updated that is why auto_now

    def __str__(self):
        return self.title
    
    
