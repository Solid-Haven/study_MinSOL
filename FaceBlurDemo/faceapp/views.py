from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
import os
from .models import User, FaceRegistration, Video
from .forms import UserForm, VideoUploadForm, RegistrationForm
from .ai.face_regis_photo  import register_face_from_image
from .ai.face_regis_video import extract_embeddings_from_webcam
from .ai.main_frame_face import main

def main_page(request):
    return render(request, 'faceapp/main.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():

            # 사용자 정보 저장
            name = form.cleaned_data['name']
            user = User.objects.create(name=name)

                # 얼굴 등록 데이터 저장
            registration_type = form.cleaned_data['registration_type']
            file = form.cleaned_data['file']
            face_registration = FaceRegistration.objects.create(
                user=user,
                registration_type=registration_type,
                file=file
            )

                # 얼굴 등록 처리
            try:
                if registration_type == 'photo' and file:
                    output_json_dir = os.path.join(settings.MEDIA_ROOT, 'face/json')
                    marked_image_dir = os.path.join(settings.MEDIA_ROOT, 'face/after_regis')
                    register_face_from_image(face_registration.file.path, output_json_dir, marked_image_dir)
                elif registration_type == 'video':
                    # 영상 처리 함수 호출
                    output_json_dir = os.path.join(settings.MEDIA_ROOT, 'face/json')
                    extract_embeddings_from_webcam(
                        output_json_path=os.path.join(output_json_dir, f"{user.id}_embeddings.json"),
                        detection_threshold=10,
                        timeout=100, 
                    )
                print("끝")
                messages.success(request, "사용자 등록 및 얼굴 등록이 완료되었습니다!")
                return redirect('upload_video', user_id=user.id)
            except Exception as e:
                messages.error(request, f"등록 중 오류가 발생했습니다: {str(e)}")
    else:
        form = RegistrationForm()

    return render(request, 'faceapp/register.html', {'form': form})



"""
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
    if request.method == 'POST':
        form = FaceRegistration(request.POST, request.FILES)
        if form.is_valid():
            # FaceRegistration 인스턴스 생성
            face_registration = form.save(commit=False)
            face_registration.user = user
            face_registration.save()

            # 업로드된 이미지 경로
            image_path = face_registration.file.path

            # 결과 디렉토리 설정
            output_json_dir = os.path.join(settings.MEDIA_ROOT, 'face/json')
            marked_image_dir = os.path.join(settings.MEDIA_ROOT, 'face/after_regis')

            # 얼굴 등록 수행
            try:
                register_face_from_image(image_path, output_json_dir, marked_image_dir)
                messages.success(request, f"{user.name}님의 얼굴이 성공적으로 등록되었습니다!")
            except Exception as e:
                messages.error(request, f"얼굴 등록 중 오류가 발생했습니다: {str(e)}")
                return redirect('register_face', user_id=user.id)

            return redirect('upload_video', user_id=user.id)
    else:
        form = FaceRegistration()

    return render(request, 'faceapp/register_face.html', {'form': form, 'user': user})
"""

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
            processed_path = main()
            if processed_path:
                processed_path = os.path.relpath(processed_path, 'media')
                video.processed_video.name = processed_path
                video.save()  # 데이터베이스에 저장
                print(f"Processed video saved: {video.processed_video.name}")
                print(f"Processed video URL: {video.processed_video.url}")
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
