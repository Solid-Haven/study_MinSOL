from django.db import models

# 사용자 모델
class User(models.Model):
    name = models.CharField(max_length=100)  # 사용자 이름
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"{self.id}: {self.name}"  # 사용자 ID와 이름 반환

# 영상 모델
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # 사용자와 연결
    original_video = models.FileField(upload_to='videos/original/', default="default_video.mp4")  # 업로드된 원본 영상
    processed_video = models.FileField(upload_to='videos/processed/', null=True, blank=True)  # 모자이크 처리된 영상
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 업로드 시간

    def __str__(self):
        return f"{self.user.name}의 업로드된 영상"
