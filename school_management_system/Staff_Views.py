from django.shortcuts import render, redirect
from app.models import staff, course, subject, student,CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def Staff_home(request):

    return render(request, 'Staff/home.html')
