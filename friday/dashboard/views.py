from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session.set_expiry(0)  # Session expires when browser closes
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'login.html')
