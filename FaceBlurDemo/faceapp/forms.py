from django import forms
from .models import User, Video

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
        

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['original_video']