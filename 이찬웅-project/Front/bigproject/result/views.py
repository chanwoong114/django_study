from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import os
import numpy as np

# Create your views here.
def result_create(request):
  if request.user.is_anonymous:
    return redirect('users:login')
  else:
    if request.method == 'POST':
      files = request.FILES.get('file')
      result = Result()
      result.create_date = datetime.now()
      result.user = request.user
      result.file = request.FILES.get('file')
      file_path = os.path.join(settings.MEDIA_ROOT, str(files))
      print(file_path)
      result.save()
      #subprocess.Popen(["python", "subprocess.py", str(files)])
        
      # separator = Separator('spleeter:2stems')
      # audio_loader = AudioAdapter.default()
      # waveform, _ = audio_loader.load(result.file.path, sample_rate=44100)
      # prediction = separator.separate(waveform)

        # path_music = 'media/'
        # os.makedirs(path_music, exist_ok=True)
        # media 폴더 -> 각 아아디 마다 폴더 -> 내가 선택한 음익 -> 분류된 음악
        # meida/ID/Music/Music_drum.mp3, Music_bass.mp3, Music.bass.mp3… 이런식으로? 

      # for inst in list(prediction.keys()):
      #   channels = 2 if (prediction[inst].ndim == 2 and prediction[inst].shape[1] == 2) else 1
      #   y = np.int16(prediction[inst] * 2 ** 15)

      #   song = pydub.AudioSegment(y.tobytes(), frame_rate=44100, sample_width=2, channels=channels)
      #   song.export('media/' + f"{name}_{inst}.mp3", format="mp3", bitrate="320k")
      
      #context = {'result': result}
      return redirect('result:result_list')
    else:
      return redirect('main')
  
def result_list(request):
  if request.user.is_anonymous:
    return redirect('users:login')
  else:
    result = Result.objects.all().order_by('-create_date') # Question 모델 데이터를 작성일시의 역순(-)으로 정렬한다.
    # Paging 기능 구현하기
    result_list = result.filter(user__username=request.user)
    page = request.GET.get('page', '1') # GET 방식 요청 URL에서 page값을 가져올 때 사용(?page=1). page 파라미터가 없는 URL을 위해 기본값으로 1을 지정한 것
    paginator = Paginator(result_list, 5) # Paginator 클래스는 questions를 페이징 객체 paginator로 변환. 페이지당 5개씩 보여주기
    page_obj = paginator.get_page(page) # page_obj 객체에는 여러 속성이 존재
    context = { 'result' : page_obj } # page_obj를 question_list에 저장한다.
    return render(request, 'result/result_list.html', context)

def file_download(request):
    path = request.GET['path']
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    print(path)
    print(file_path)
    if os.path.exists(file_path):
        binary_file = open(file_path, 'rb')
        response = HttpResponse(binary_file.read(), content_type="application/octet-stream; charset=utf-8")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    else:
        message = '알 수 없는 오류가 발생하였습니다.'
        return HttpResponse("<script>alert('"+ message +"');history.back()'</script>")
      
def result_detail(request, result_id):
  result = get_object_or_404(Result, pk=result_id)
  
  context = { 'result' : result }
  returns = []
  
  for i in range(1, 16):
    path = 'media/' + result.file.name + '-' + str(i) + '.png'
    print(path)
    if os.path.exists(path):
      returns.append("../" + path)
      
  context['ret'] = returns
  context['mid'] = str(result.file.name) + '.mid'
  context['mp3'] = str(result.file.name)
  
  return render(request, 'result/result.html', context)