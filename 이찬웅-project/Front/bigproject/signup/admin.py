from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin) : # QuestionAdmin 클래스를 추가
  list_display = ( # 목록에서 보여줄 column
    'username',
    'email',
  )
  search_fields = [ # 검색이 가능한 column
    'username',
  ]

admin.site.register(User, UserAdmin)