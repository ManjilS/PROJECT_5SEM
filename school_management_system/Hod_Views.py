from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import course, session_year, student,CustomUser,staff,subject
from django.contrib import messages
from django.shortcuts import get_object_or_404



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


def add_staff(request):
    return render(request, 'Hod/add_staff.html')

def view_staff(request):
    return render(request, 'Hod/view_staff.html')
def VIEW_STUDENT(request):
    students = student.objects.all()
    context = {
        'students': students,
    }
    return render(request, 'Hod/view_student.html', context)
  
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

def view_course(request):
    courses = course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'Hod/view_course.html', context)




def edit_course(request,id):
    course_id = course.objects.get(id=id)
    context = {
        'course': course_id,
    }
    return render(request, 'Hod/edit_course.html',context)

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

def delete_course(request, id):
    course_obj = course.objects.get(id=id)
    course_obj.delete()
    messages.success(request, 'Course deleted successfully')
    return redirect('view_course')




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



def view_staff(request):
    staff_members = staff.objects.all()
    context = {
        'staff_members': staff_members,
    }

    return render(request, 'Hod/view_staff.html',context)



def edit_staff(request,id):
    staff_id = staff.objects.get(id=id)
    context = {
        'staff': staff_id,
    }
    return render(request, 'Hod/edit_staff.html',context)

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

def view_subject(request):

    subject_obj = subject.objects.all()
    context = {
        'subject_obj': subject_obj,
    }
    return render(request, 'Hod/view_subject.html',context)