from django import forms
from .models import User, FaceRegistration, Video

class UserForm(forms.ModelForm):
    class Meta: 
        model = User
        fields = ['name']
        labels = {
            'name': '이름',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '이름을 입력하세요'}),
        }

class FaceRegistrationForm(forms.ModelForm):
    class Meta:
        model = FaceRegistration
        fields = ['registration_type', 'file']
        labels = {
            'registration_type': '등록 방식',
            'file': '파일 업로드',
        }
        widgets = {
            'registration_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        

class RegistrationForm(forms.Form):
    # 사용자 정보 필드
    name = forms.CharField(max_length=100, label='사용자 이름', widget=forms.TextInput(attrs={'class': 'form-control'}))

    # 얼굴 등록 필드
    REGISTRATION_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
    ]
    registration_type = forms.ChoiceField(choices=REGISTRATION_TYPE_CHOICES, label='등록 방식', widget=forms.Select(attrs={'class': 'form-control'}))
    file = forms.FileField(label='파일 업로드', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)



class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['original_video']