from django.shortcuts import render

# index.html 페이지를 부르는 index 함수
def index(request):
    return render(request,'index.html')

# blog.html 페이지를 부르는 blog 함수
def blog(request):
    return render(request, 'blog.html')