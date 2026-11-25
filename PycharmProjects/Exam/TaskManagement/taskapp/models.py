from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TaskDb(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    due_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=50,default="pending")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")

    def __str__(self):
        return self.user


