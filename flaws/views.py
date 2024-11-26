from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from .models import User
import hashlib
import time

def index(request):
    session_token = request.COOKIES.get('session_token')
    print(session_token)
    if not session_token:
        return redirect('flaws:login')
    
    try:
        user = User.objects.get(session_token=session_token)
        return render(request, 'index.html', {'user': user})
    except User.DoesNotExist:
        return redirect('flaws:login')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            #from django.contrib.auth.hashers import make_password
            #user.password = make_password(password)  # Hash the password
            user.password = password
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('flaws:login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(request)

        try:
            user = User.objects.get(username=username)

            if (password == user.password):
                print("password matched", password, user.password)
                session_token = hashlib.sha256(f'{username}{time.time()}'.encode()).hexdigest()
                response = redirect('flaws:index')
                response.set_cookie('session_token', session_token, max_age=3600)
                user.session_token = session_token
                user.save()
                messages.success(request, "Login successful!")
                return response
            else:
                messages.error(request, "Invalid username or password.")
        except User.DoesNotExist:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

def logout(request):
    response = HttpResponse('Logged out successfully!')
    response.delete_cookie('session_token')
    return redirect('flaws:login')