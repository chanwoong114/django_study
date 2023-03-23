from django.contrib import admin
from .models import Question

class QuestionAdmin(admin.ModelAdmin) : # QuestionAdmin 클래스를 추가
  list_display = ( # 목록에서 보여줄 column
    'subject',
    'content',
    'create_date',
    'imgfile',
    'user'
  )
  search_fields = [ # 검색이 가능한 column
    'subject',
  ]

admin.site.register(Question, QuestionAdmin)
