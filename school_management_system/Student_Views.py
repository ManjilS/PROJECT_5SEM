from django.shortcuts import render, redirect,HttpResponse

def student_register(request):
    if request.method == 'POST':
        # handle form submission here
        # e.g., save to DB
        return HttpResponse("Student registered successfully!")
    return render(request, 'student_register.html')  # or whatever your template is
def student(request):
    return render(request,'student.html')
