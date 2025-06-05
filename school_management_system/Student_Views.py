from django.shortcuts import render, redirect

from app.models import course, session_year, student,CustomUser,staff,subject,student_notification



def Student_home(request):
    
        return render(request, 'Student/home.html', {'message': 'Student logged in successfully!'})

def Student_notification(request):
    student_obj = student.objects.filter(admin=request.user.id)
    for i in student_obj:
        student_id =i.id
    student_notification_obj = student_notification.objects.filter(student_id=student_id)
    context = {
        'student_notification_obj': student_notification_obj,
    }
    return render(request, 'Student/student_notification.html',context)


def Student_mark_as_done(request,status):
    notificaion_obj = student_notification.objects.get(id=status)
    notificaion_obj.status = 1

    notificaion_obj.save()
    return redirect('student_notification')