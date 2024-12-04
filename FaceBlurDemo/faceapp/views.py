from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import User, Video
from .forms import UserForm, VideoUploadForm
from .ai.face_registration import register_face
from .ai.face_masking import process_video

def main_page(request):
    return render(request, 'faceapp/main.html')

# 1. 사용자 등록
def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('register_face', user_id=user.id)
    else:
        form = UserForm()
    return render(request, 'faceapp/register_user.html', {'form': form})

# 2. 얼굴 등록
def register_face_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        register_face(user.id)  # 얼굴 등록 AI 코드 호출
        return JsonResponse({'message': f"사용자 {user.name}의 얼굴이 성공적으로 등록되었습니다."})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# 3. 영상 업로드 및 처리
def upload_video(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = user
            video.save()

            # AI 영상 처리
            processed_path = process_video(video.original_video.path, user.id)
            if processed_path:
                video.processed_video.name = processed_path
                video.save()  # 데이터베이스에 저장
                print(f"Processed video saved: {video.processed_video.name}")
            else:
                print("Error processing video")
                
            return redirect('video_list', user_id=user.id)
    else:
        form = VideoUploadForm()
    return render(request, 'faceapp/upload_video.html', {'form': form, 'user': user})

# 4. 영상 목록
def video_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    videos = Video.objects.filter(user=user).order_by('-uploaded_at')
    return render(request, 'faceapp/video_list.html', {'videos': videos, 'user': user})

# 특정 영상 보기
def view_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'faceapp/view_video.html', {'video': video})
