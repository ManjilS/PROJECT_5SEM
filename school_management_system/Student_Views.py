from django.shortcuts import render, redirect
def Student_home(request):
    return render(request, 'Student/home.html')