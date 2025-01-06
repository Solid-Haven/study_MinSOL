from django.db import models

# 사용자 모델
class User(models.Model):
    name = models.CharField(max_length=100)  # 사용자 이름
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"{self.id}: {self.name}"  # 사용자 ID와 이름 반환

# 얼굴 등록 모델
class FaceRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 한 사용자당 한 번 등록 (User모델이랑 1:1관계)
    registration_type = models.CharField(   # 얼굴 등록 방식 저장 
        max_length=10,
        choices=[('photo', 'Photo'), ('video', 'Video')],
        default='photo'
    )
    file = models.FileField(upload_to='face/before_regis/', null=True, blank=True)  # 등록된 사진 또는 영상
    registered_at = models.DateTimeField(auto_now_add=True)  # 등록 시간

    def __str__(self):
        return f"{self.user.name} - {self.get_registration_type_display()} 등록"

# 영상 모델
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # 사용자와 연결
    original_video = models.FileField(upload_to='before/', default="default_video.mp4")  # 업로드된 원본 영상
    processed_video = models.FileField(upload_to='after/', null=True, blank=True)  # 모자이크 처리된 영상
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 업로드 시간

    def __str__(self):
        return f"{self.user.name}의 업로드된 영상"
