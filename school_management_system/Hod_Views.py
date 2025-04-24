from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def home(request):
    return render(request, 'Hod/home.html')

@login_required(login_url='/')
def myprofile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'Hod/myprofile.html', context)
@login_required(login_url='/')
def add_student(request):

    return render(request, 'Hod/add_student.html')