from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit

class Chat(models.Model):
    user = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(
        blank=True,
        processors=[ResizeToFit(200,200)],
        format='JPEG',
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFit(100,100)],
        format="JPEG",
        options={'quality':90},
    )
    