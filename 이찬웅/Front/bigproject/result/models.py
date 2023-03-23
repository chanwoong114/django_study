from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    create_date = models.DateTimeField(auto_now = True)
    file = models.FileField(null=True, upload_to='files')
    # 0=None
    # 1=대기중
    # 2=변환중
    # 3=변환완료
    status = models.IntegerField(default=1)
    instrument = models.IntegerField(default=1)