from django.urls import reverse
from django.db import models

# Create your models here.
class Chatting(models.Model):
    user = models.CharField(max_length=10)
    content = models.TextField()

    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
    
    def get_absolute_url(self):
        return reverse("chatting:detail", kwargs={"pk": self.pk})
    
    def get_previous(self):
        return self.get_previous_by_created_at()
    
    def get_next(self):
        return self.get_next_by_created_at()
    