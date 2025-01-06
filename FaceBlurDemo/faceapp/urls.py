from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='home'),  # 루트 URL을 사용자 등록 뷰로 연결
    path('register/', views.register, name='register'),  # 얼굴 등록
    path('upload-video/<int:user_id>/', views.upload_video, name='upload_video'),  # 영상 업로드
    path('video-list/<int:user_id>/', views.video_list, name='video_list'),  # 영상 목록
    path('videos/<int:video_id>/', views.view_video, name='view_video'),  # 특정 영상 보기
    
]