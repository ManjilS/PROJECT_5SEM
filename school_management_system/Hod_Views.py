from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app.models import course, session_year, result,staff_leave,student,CustomUser,staff,subject,staff_notification,staff_feedback,student_notification,student_feedback,student_leave,attendance, attendance_report
from django.contrib import messages
from django.shortcuts import get_object_or_404



@login_required(login_url='/')
def home(request):
    student_count = student.objects.all().count()
    staff_count = staff.objects.all().count()
    course_count = course.objects.all().count()
    subject_count = subject.objects.all().count()
    male_student_count = student.objects.filter(gender='Male').count()
    female_student_count = student.objects.filter(gender='Female').count()

    # 👇 Add student details
    all_students = student.objects.select_related('course_id').all()
    if student_count > 0:
        male_percentage = round(male_student_count / student_count * 100, 2)
        female_percentage = round(female_student_count / student_count * 100, 2)
    else:
        male_percentage = 0
        female_percentage = 0

    context = {
        'student_count': student_count,
        'staff_count': staff_count,
        'course_count': course_count,
        'subject_count': subject_count,
        'male_student_count': male_student_count,
        'female_student_count': female_student_count,
        'all_students': all_students,  # 👈 Include this
        'male_percentage':male_percentage,
        'female_percentage':female_percentage,
    }

    return render(request, 'Hod/home.html', context)


@login_required(login_url='/')
def myprofile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'Hod/myprofile.html', context)

@login_required(login_url='/')
def add_student(request):
    
    courses = course.objects.all()
    session_years = session_year.objects.all()

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password') 
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        gender = request.POST.get('gender') 
        selected_course_id = request.POST.get('course')  
        selected_session_year_id = request.POST.get('session_year')

        # Normalize email
        email = email.lower().strip()

        # Validate unique fields
       
        if CustomUser.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('add_student')
        
        
        # Normalize username
        username = username.lower().strip()

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('add_student')

        # Create user
        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,    
            
            profile_pic=profile_pic,
            user_type=3,
        )
        user.set_password(password)
        user.save()

        # Get related objects
        selected_course = course.objects.get(id=selected_course_id)
        selected_session_year = session_year.objects.get(id=selected_session_year_id)

        # Create student
        students = student(
            admin=user,
            address=address,
            phone_number=phone_number,
            gender=gender,
            course_id=selected_course,
            session_year_id=selected_session_year
        )
        students.save()


        messages.success(request, 'Student added successfully')
        return redirect('add_student')

    context = {
        'courses': courses,
        'session_years': session_years,
    }
    return render(request, 'Hod/add_student.html', context)

@login_required(login_url='/')
def add_staff(request):
    return render(request, 'Hod/add_staff.html')

@login_required(login_url='/')
def view_staff(request):
    return render(request, 'Hod/view_staff.html')

@login_required(login_url='/')
def VIEW_STUDENT(request):
    students = student.objects.all()
    context = {
        'students': students,
    }
    return render(request, 'Hod/view_student.html', context)
@login_required(login_url='/')
def edit_student(request,id):
    student_id = student.objects.get(id=id)
    courses = course.objects.all()
    session_years = session_year.objects.all()
    context = {
        'student': student_id,
        'courses': courses,
        'session_years': session_years,
    }
    return render(request, 'Hod/edit_student.html',context)
@login_required(login_url='/')
def update_student(request):
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password') 
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        gender = request.POST.get('gender') 
        selected_course_id = request.POST.get('course')  
        selected_session_year_id = request.POST.get('session_year')

        student_obj = student.objects.get(id=student_id)
        user = CustomUser.objects.get(id=student_obj.admin.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        
        if password != " ":
            user.set_password(password)
        if profile_pic != " ":
            user.profile_pic = profile_pic

        user.save()
        student_obj = student.objects.get(id=student_id)
        student_obj.address = address
        student_obj.phone_number = phone_number
        student_obj.gender=gender
        courses= course.objects.get(id=selected_course_id)
        student_obj.course_id=courses
        session_years= session_year.objects.get(id=selected_session_year_id)
        student_obj.session_year_id=session_years

        student_obj.save()
        messages.success(request, 'Student updated successfully')
        return redirect('view_student')

    return render(request, 'Hod/edit_student.html')

@login_required(login_url='/')
def delete_student(request, admin):
    user = CustomUser.objects.get(id=admin)
    try:
        # Delete the related student object first
        student_obj = student.objects.get(admin=user)
        student_obj.delete()
        # Then delete the user
        user.delete()
        messages.success(request, 'Student deleted successfully')
    except student.DoesNotExist:
        messages.error(request, 'Student record not found')
    except Exception as e:
        messages.error(request, f'Error occurred: {str(e)}')
    return redirect('view_student')

@login_required(login_url='/')
def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_code = request.POST.get('course_code')

        # Check if the course already exists
        if course.objects.filter(course_name__iexact=course_name).exists():
            messages.error(request, 'Course with this name already exists')
            return redirect('add_course')

        if course.objects.filter(course_code__iexact=course_code).exists():
            messages.error(request, 'Course with this code already exists')
            return redirect('add_course')

        if not course_code:
            messages.error(request, 'Course code is required')
            return redirect('add_course')

        course_obj = course(
            course_name=course_name,
            course_code=course_code
        )
        course_obj.save()
        messages.success(request, 'Course added successfully')
        return redirect('add_course')
    context = {}    
    return render(request, 'Hod/add_course.html', context)
@login_required(login_url='/')
def view_course(request):
    courses = course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'Hod/view_course.html', context)



@login_required(login_url='/')
def edit_course(request,id):
    course_id = course.objects.get(id=id)
    context = {
        'course': course_id,
    }
    return render(request, 'Hod/edit_course.html',context)
@login_required(login_url='/')
def update_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course_name')
        course_code = request.POST.get('course_code')

        course_obj = course.objects.get(id=course_id)
        course_obj.course_name = course_name
        course_obj.course_code = course_code
        course_obj.save()
        messages.success(request, 'Course updated successfully')
        return redirect('view_course')

    return render(request, 'Hod/edit_course.html')
@login_required(login_url='/')
def delete_course(request, id):
    course_obj = course.objects.get(id=id)
    course_obj.delete()
    messages.success(request, 'Course deleted successfully')
    return redirect('view_course')



@login_required(login_url='/')
def add_staff(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password') 

        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

    # Normalize email   
        email = email.lower().strip()
            # Normalize username
        username = username.lower().strip()

        if CustomUser.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('add_staff')
        
    
        user=CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,    
            
            profile_pic=profile_pic,
            user_type=2,
        )
        user.set_password(password)
        user.save()

        staff_obj=staff(
            admin=user,
            address=address,
            phone_number=phone_number,
            gender=gender
        )
        staff_obj.save()
        messages.success(request, 'Staff added successfully')
        return redirect('add_staff')

    return render(request, 'Hod/add_staff.html')


@login_required(login_url='/')
def view_staff(request):
    staff_members = staff.objects.all()
    context = {
        'staff_members': staff_members,
    }

    return render(request, 'Hod/view_staff.html',context)


@login_required(login_url='/')
def edit_staff(request,id):
    staff_id = staff.objects.get(id=id)
    context = {
        'staff': staff_id,
    }
    return render(request, 'Hod/edit_staff.html',context)
@login_required(login_url='/')
def update_staff(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password') 
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        staff_obj = staff.objects.get(id=staff_id)
        user=CustomUser.objects.get(id=staff_obj.admin.id)
        
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        
        if password != " ":
            user.set_password(password)
        if profile_pic != " ":
            user.profile_pic = profile_pic

        user.save()

        staff_obj = staff.objects.get(id=staff_id)
        staff_obj.address = address
        staff_obj.phone_number = phone_number
        staff_obj.gender=gender

        staff_obj.save()
        messages.success(request, 'Staff updated successfully')
        return redirect('view_staff')
    return render(request, 'Hod/edit_staff.html')

@login_required(login_url='/')
def delete_staff(request, admin):
    user = CustomUser.objects.get(id=admin)
    try:
        # Delete the related staff object first
        staff_obj = staff.objects.get(admin=user)
        staff_obj.delete()
        # Then delete the user
        user.delete()
        messages.success(request, 'Staff deleted successfully')
    except staff.DoesNotExist:
        messages.error(request, 'Staff record not found')
    except Exception as e:
        messages.error(request, f'Error occurred: {str(e)}')
    return redirect('view_staff')

@login_required(login_url='/')
def add_subject(request):
    courses = course.objects.all()
    staff_members = staff.objects.all()

    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        selected_course_id = request.POST.get('course_id')  
        selected_staff_id = request.POST.get('staff_id')

        
        course_obj = course.objects.get(id=selected_course_id)
        staff_obj = staff.objects.get(id=selected_staff_id)

        subject_obj = subject(
            subject_name=subject_name,
            subject_code=subject_code,
            course_id=course_obj,
            staff_id=staff_obj
        )
        subject_obj.save()
        messages.success(request, 'Subject added successfully')
        return redirect('add_subject')

    context = {
        'courses': courses,
        'staff_members': staff_members,
    }
    return render(request, 'Hod/add_subject.html', context)
@login_required(login_url='/')
def view_subject(request):

    subject_obj = subject.objects.all()
    context = {
        'subject_obj': subject_obj,
    }
    return render(request, 'Hod/view_subject.html',context)
@login_required(login_url='/')
def edit_subject(request,id):
    subject_id = subject.objects.get(id=id)
    courses = course.objects.all()
    staff_members = staff.objects.all()
    context = {
        'subject': subject_id,
        'courses': courses,
        'staff_members': staff_members,
    }
    return render(request, 'Hod/edit_subject.html',context)
@login_required(login_url='/')
def update_subject(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        selected_course_id = request.POST.get('course_id')
        selected_staff_id = request.POST.get('staff_id')

        course_obj = course.objects.get(id=selected_course_id)
        staff_obj = staff.objects.get(id=selected_staff_id)

        subject_obj = subject(
            id=subject_id,
            subject_name=subject_name,
            subject_code=subject_code,
            course_id=course_obj,
            staff_id=staff_obj

        )
        subject_obj.save()
        messages.success(request, 'Subject updated successfully')
        
    return redirect('view_subject')
@login_required(login_url='/')
def delete_subject(request, id):
    subject_obj = subject.objects.get(id=id)
    subject_obj.delete()    
    messages.success(request, 'Subject deleted successfully')
    return redirect('view_subject')

@login_required(login_url='/')
def add_session(request):
    if request.method == 'POST':
        session_start_year = request.POST.get('start_date')
        session_end_year = request.POST.get('end_date')

        # Check if the session year already exists
        if session_year.objects.filter(session_start_year=session_start_year, session_end_year=session_end_year).exists():
            messages.error(request, 'Session year already exists')
            return redirect('add_session')

        session_obj = session_year(
            session_start_year=session_start_year,
            session_end_year=session_end_year
        )
        session_obj.save()
        messages.success(request, 'Session year added successfully')
        return redirect('add_session')
    return render(request, 'Hod/add_session.html')

@login_required(login_url='/')
def view_session(request):
    session_years = session_year.objects.all()
    context = {
        'session_years': session_years,
    }
    return render(request, 'Hod/view_session.html', context)

@login_required(login_url='/')
def edit_session(request,id):
    session_obj = session_year.objects.get(id=id)
    context = {
        'session': session_obj,
    }
    return render(request, 'Hod/edit_session.html',context)
@login_required(login_url='/')
def update_session(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('start_date')
        session_end_year = request.POST.get('end_date')

        session_obj = session_year.objects.get(id=session_id)
        session_obj.session_start_year = session_start_year
        session_obj.session_end_year = session_end_year
        session_obj.save()
        messages.success(request, 'Session updated successfully')
        return redirect('view_session')

    return render(request, 'Hod/edit_session.html')
@login_required(login_url='/')
def delete_session(request, id):
    session_obj = session_year.objects.get(id=id)
    session_obj.delete()
    messages.success(request, 'Session deleted successfully')
    return redirect('view_session')
@login_required(login_url='/')
def send_staff_notification(request):
    staff_members = staff.objects.all()
    see_notification = staff_notification.objects.all().order_by('-id')[0:5]
    context = {
        'staff_members': staff_members,
        'see_notification': see_notification,
    }
    
    return render(request, 'Hod/send_staff_notification.html',context)

@login_required(login_url='/')
def save_staff_notification(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff_obj = staff.objects.get(admin=staff_id)
        notification =staff_notification(
            staff_id=staff_obj,
            message=message
        )

        # Save the notification to the user's profile
        
        notification.save()

        messages.success(request, 'Notification sent successfully')
        return redirect('send_staff_notification')

    return render(request, 'Hod/send_staff_notification.html')
@login_required(login_url='/')   
def view_staff_leave(request):
    staff_leave_obj = staff_leave.objects.all()
    context = {
        'staff_leave_obj': staff_leave_obj,
    }
    return render(request, 'Hod/view_staff_leave.html',context)

@login_required(login_url='/')
def staff_approve_leave(request, id):
    staff_leave_obj = staff_leave.objects.get(id=id)
    staff_leave_obj.leave_status = 1
    staff_leave_obj.save()
    messages.success(request, 'Leave approved successfully')
    return redirect('view_staff_leave')

@login_required(login_url='/')
def staff_disapprove_leave(request, id):
    staff_leave_obj = staff_leave.objects.get(id=id)
    staff_leave_obj.leave_status = 2
    staff_leave_obj.save()
    messages.success(request, 'Leave disapproved successfully')
    return redirect('view_staff_leave')

def views_staff_feedback(request): 
    feedback = staff_feedback.objects.all() 

    context = {
        'feedback': feedback, 
    }
    return render(request, 'Hod/staff_feedback.html', context)

def views_staff_feedback_save(request):
   if request.method == 'POST':
         feedback_id=request.POST.get('feedback_id')
         feedback_reply = request.POST.get('feedback_reply')
         
         
         feedback = staff_feedback.objects.get(id=feedback_id)
         feedback.feedback_reply= feedback_reply
         feedback.save()
         messages.success(request, "Feedback send successfully")
         return redirect('staff_feedback_reply')

@login_required(login_url='/')
def send_student_notification(request):
    students = student.objects.all()
    see_notification = student_notification.objects.all().order_by('-id')[0:5]
    context = {
        'students': students,
        'see_notification': see_notification,
    }
    
    return render(request, 'Hod/send_student_notification.html',context)

@login_required(login_url='/')
def save_student_notification(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        message = request.POST.get('message')

        student_obj = student.objects.get(admin=student_id)
        notification =student_notification(
            student_id=student_obj,
            message=message
        )

        # Save the notification to the user's profile
        
        notification.save()

        messages.success(request, 'Notification sent successfully')
        return redirect('send_student_notification')

    return render(request, 'Hod/send_student_notification.html')

def view_student_leave(request):
    student_leave_obj = student_leave.objects.all()
    context = {
        'student_leave_obj': student_leave_obj,
    }
    return render(request, 'Hod/view_student_leave.html',context)

@login_required(login_url='/')
def student_approve_leave(request, id):
    student_leave_obj = student_leave.objects.get(id=id)
    student_leave_obj.leave_status = 1
    student_leave_obj.save()
    messages.success(request, 'Leave approved successfully')
    return redirect('view_student_leave')

@login_required(login_url='/')
def student_disapprove_leave(request, id):
    student_leave_obj = student_leave.objects.get(id=id)
    student_leave_obj.leave_status = 2
    student_leave_obj.save()
    messages.success(request, 'Leave disapproved successfully')
    return redirect('view_student_leave')


def views_student_feedback(request): 
    feedback = student_feedback.objects.all() 

    context = {
        'feedback': feedback, 
    }
    return render(request, 'Hod/student_feedback.html', context)

def views_student_feedback_save(request):
   if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        try:
            feedback = student_feedback.objects.get(id=feedback_id)
            feedback.feedback_reply = feedback_reply
            feedback.save()
            messages.success(request, "Feedback sent successfully.")
        except student_feedback.DoesNotExist:
            messages.error(request, "Feedback not found.")

        return redirect('student_feedback_reply')


def view_attendance(request):
    
    subject_obj = subject.objects.all()
    session_year_obj = session_year.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_session = None
    attendance_date = None
    attendance_report_obj = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_id = request.POST.get('session_id')
            attendance_date = request.POST.get('attendance_date')

            get_subject = subject.objects.get(id=subject_id)
            get_session = session_year.objects.get(id=session_id)

            attendance_obj = attendance.objects.filter(
                subject_id=get_subject,
                attendance_date=attendance_date,
                session_year_id=get_session,
                
            )
            for i in attendance_obj:
                attendance_id = i.id
                attendance_report_obj = attendance_report.objects.filter(attendance_id=attendance_id)
           

           

    context= {
        'subject_obj': subject_obj,
        'session_year_obj': session_year_obj,
        'action': action,
        'get_subject': get_subject,
        'get_session': get_session,
        'attendance_date': attendance_date,
        'attendance_report_obj': attendance_report_obj ,
    }
    
    return render(request, 'Hod/hod_view_attendance.html',context)

def view_result(request):
    subject_obj = subject.objects.all()
    session_year_obj = session_year.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_session = None
    student_obj = None
    result_obj = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_id = request.POST.get('session_id')

            get_subject = subject.objects.get(id=subject_id)
            get_session = session_year.objects.get(id=session_id)

            student_obj = student.objects.filter(course_id=get_subject.course_id, session_year_id=get_session)
            result_obj = result.objects.filter(student_id__in=student_obj, subject_id=get_subject)

    context= {
        'subject_obj': subject_obj,
        'session_year_obj': session_year_obj,
        'action': action,
        'get_subject': get_subject,
        'get_session': get_session,
        'student_obj': student_obj,
        'result_obj': result_obj,
    }
    
    return render(request, 'Hod/hod_view_result.html',context)