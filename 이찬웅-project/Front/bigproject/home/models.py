from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200, null = False) 
    content = models.TextField() 
    create_date = models.DateTimeField(auto_now = True)
    imgfile = models.ImageField(null=True, upload_to="images", blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    updated_at = models.DateTimeField(auto_now=True)
  
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    
class Sheet(models.Model):
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)
    imgfile = models.ImageField()