from django.shortcuts import render, redirect


from app.models import course, session_year, student,CustomUser,staff,result,subject,student_notification,student_feedback,student_leave,attendance,attendance_report
from django.contrib import messages


def Student_home(request):
    student_obj = student.objects.get(admin=request.user)

    # Get all subjects for student's course & session year (assuming course-subject relation exists)
    subjects = student_obj.course_id.subject_set.all()

    subject_attendance = []

    for subj in subjects:
        # All attendance sessions for this subject and student's session year
        total_sessions = attendance_report.objects.filter(
            student_id=student_obj.id,
            attendance_id__subject_id=subj.id,
            attendance_id__session_year_id=student_obj.session_year_id
        ).count()

        # Present count for this subject
        present_sessions = attendance_report.objects.filter(
            student_id=student_obj.id,
            attendance_id__subject_id=subj.id,
            attendance_id__session_year_id=student_obj.session_year_id,
            is_present=True
        ).count()

        percentage = (present_sessions / total_sessions * 100) if total_sessions > 0 else None

        subject_attendance.append({
            'subject_name': subj.subject_name,
            'present': present_sessions,
            'total': total_sessions,
            'percentage': percentage,
        })

    notification_obj = student_notification.objects.filter(student_id=student_obj.id).order_by('-id')

    context = {
        'student_obj': student_obj,
        'subject_attendance': subject_attendance,
        'notification_obj': notification_obj,
    }
    return render(request, 'Student/home.html', context)

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
    
def student_view_attendance(request):
    student_obj = student.objects.get(admin=request.user.id)
    subject_obj = subject.objects.filter(course_id=student_obj.course_id)

    action = request.GET.get('action')
    get_subject = None
    attendance_report_obj = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            get_subject = subject.objects.get(id=subject_id)

           
            attendance_report_obj = attendance_report.objects.filter(student_id=student_obj,attendance_id__subject_id=get_subject)
    
    context = {
        'subject_obj': subject_obj,
        'action': action,
        'get_subject': get_subject,
        'attendance_report_obj': attendance_report_obj,
    }
    return render(request, 'Student/student_view_attendance.html', context)

def student_view_result(request):
    student_obj = student.objects.get(admin=request.user.id)
    result_obj = result.objects.filter(student_id=student_obj)
    for i in result_obj:
        assignment_marks = i.assignment_marks
        ut_marks = i.ut_marks
        assessment_marks = i.assessment_marks
    context = {
        'result_obj': result_obj,
        'assignment_marks': assignment_marks,
        'ut_marks': ut_marks,
        'assessment_marks': assessment_marks,
    }
    return render(request, 'Student/student_view_result.html', context)

