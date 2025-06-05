from django.shortcuts import render, redirect
from app.models import course, session_year, student,CustomUser,staff,subject


def Student_home(request):
    user = CustomUser.objects.get(id=request.user.id)
    student_obj = student.objects.get(admin=user)
    
    context = {
        'student': student_obj,
        'user': user,
    }
    return render(request, 'Student/home.html',context)