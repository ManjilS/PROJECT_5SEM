from django.shortcuts import render, redirect

from app.models import course, session_year, student,CustomUser,staff,subject,student_notification,student_leave
from django.contrib import messages


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

def Student_leave(request):
    
    student_obj = student.objects.filter(admin=request.user.id)
    for i in student_obj:
        student_id = i.id
    
    
    student_leave_obj = student_leave.objects.filter(student_id=student_id) # Gets the first record or None
    
    

    context = {
        'student_leave_obj': student_leave_obj,
    }
    return render(request, 'Student/student_leave.html', context)

def Student_leave_save(request):
    if request.method == 'POST':
        leave_start_date = request.POST.get('leave_start_date')
        leave_end_date = request.POST.get('leave_end_date')
        reason = request.POST.get('reason')

        student_obj = student.objects.get(admin=request.user.id)
        student_leave_obj = student_leave(
            student_id=student_obj,
            leave_start_date=leave_start_date, 
            leave_end_date=leave_end_date,
            leave_message=reason
        )
        student_leave_obj.save()
        messages.success(request, "Leave applied successfully")
        return redirect('student_leave')
    return None