from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import course, session_year, student,CustomUser
from django.contrib import messages
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
    # Ensure model names start with capital letters: Course, SessionYear, Student
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
