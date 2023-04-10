from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    upload = models.FileField(upload_to='images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # 비밀번호 암호화
        self.password = make_password(self.password)

        super().save(*args, **kwargs)