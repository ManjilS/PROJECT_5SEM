from django.shortcuts import render, redirect, HttpResponse
from app.EmailBackEnd import EmailBackend
from django.contrib.auth import authenticate, login as auth_login, logout 

def base(request):
    return render(request, 'base.html')

def login_view(request):  
    return render(request, 'login.html')

def doLogin(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = EmailBackend.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  
            user_type = user.user_type
            if user_type == '1':
                return HttpResponse("This is HOD page")
            elif user_type == '2':
                return HttpResponse("This is Staff page")
            elif user_type == '3':
                return HttpResponse("This is Student panel husdihgkhi")
            else:
                return redirect('login')
        else:
            return redirect('login')
