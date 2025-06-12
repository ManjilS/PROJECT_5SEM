from django.shortcuts import render, redirect

from app.models import course, session_year, student,CustomUser,staff,subject,student_notification,student_feedback
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

def Student_feedback(request ):

    student_id= student.objects.get(admin=request.user.id)
    feedback_history = student_feedback.objects.filter(student_id = student_id )
    context = {
        'feedback_history': feedback_history,
    }
    return render(request, 'student/feedback.html',context)

def Student_feedback_save(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        student_id = student.objects.get(admin=request.user.id)  # Declare here or earlier in the function

        feedback= student_feedback(
            student_id=student_id,
            feedback=feedback,
            feedback_reply="",
        )
        feedback.save()

        messages.success(request, "Feedback submitted successfully")
        return redirect('student_feedback')