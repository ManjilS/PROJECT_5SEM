from django.shortcuts import render, redirect
from app.models import staff, course, subject, student,CustomUser,staff_leave,staff_notification,staff_feedback
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def Staff_home(request):

    return render(request, 'Staff/home.html')

@login_required(login_url='/')
def Staff_notification(request):
    staff_obj = staff.objects.filter(admin=request.user.id)
    for i in staff_obj:
        staff_id =i.id
    staff_notification_obj = staff_notification.objects.filter(staff_id=staff_id)
    context = {
        'staff_notification_obj': staff_notification_obj,
    }
    return render(request, 'Staff/staff_notification.html',context)

@login_required(login_url='/')
def Staff_mark_as_done(request,status):
    notificaion_obj = staff_notification.objects.get(id=status)
    notificaion_obj.status = 1

    notificaion_obj.save()
    return redirect('staff_notification')

@login_required(login_url='/')
def Staff_apply_leave(request):
    
    staff_obj = staff.objects.filter(admin=request.user.id)
    for i in staff_obj:
        staff_id = i.id
    
    
    staff_leave_obj = staff_leave.objects.filter(staff_id=staff_id) # Gets the first record or None
    
    

    context = {
        'staff_leave_obj': staff_leave_obj,
    }
    return render(request, 'Staff/apply_leave.html', context)

@login_required(login_url='/')
def Staff_apply_leave_save(request):
    if request.method == 'POST':
        leave_start_date = request.POST.get('leave_start_date')
        leave_end_date = request.POST.get('leave_end_date')
        reason = request.POST.get('reason')

        staff_obj = staff.objects.get(admin=request.user.id)
        staff_leave_obj = staff_leave(
            staff_id=staff_obj,
            leave_start_date=leave_start_date,
            leave_end_date=leave_end_date,
            leave_message=reason
        )
        staff_leave_obj.save()
        messages.success(request, "Leave applied successfully")
        return redirect('staff_apply_leave')
    return None

@login_required(login_url='/')
def Staff_feedback(request ):

    staff_id= staff.objects.get(admin=request.user.id)
    feedback_history = staff_feedback.objects.filter(staff_id=staff_id)
    context = {
        'feedback_history': feedback_history,
    }
    return render(request, 'Staff/feedback.html',context)



def Staff_feedback_save(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        staff_id = staff.objects.get(admin=request.user.id)  # Declare here or earlier in the function

        feedback= staff_feedback(
            staff_id=staff_id,
            feedback=feedback,
            feedback_reply="",
        )
        feedback.save()

        messages.success(request, "Feedback submitted successfully")
        return redirect('staff_feedback')  # Redirect to the correct URL if necessary
