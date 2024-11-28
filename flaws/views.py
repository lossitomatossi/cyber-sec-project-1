from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from .forms import UserRegistrationForm
from django.contrib import messages
from .models import User, Pet
import hashlib
import time
from django.db import connection


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
        user = form.save(commit=False)
        password = form.cleaned_data['password1']
        #from django.contrib.auth.hashers import make_password
        #user.password = make_password(password)  # Hash the password
        user.password = password
        user.save()
        return redirect('flaws:login')
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

#from django.contrib.auth import authenticate, login
#def login(request):
#    if request.method == 'POST':
#        username = request.POST['username']
#        password = request.POST['password']
#
#        # Authenticate the user using Django's authenticate function
#        user = authenticate(request, username=username, password=password)
#
#        if user is not None:
#            # If user is authenticated, log them in (this handles session management)
#            login(request, user)
#
#            # Optionally, set a custom message or redirect
#            messages.success(request, "Login successful!")
#            return redirect('flaws:index')  # Redirect to the index page or dashboard
#        else:
#            messages.error(request, "Invalid username or password.")
#    
#    return render(request, 'login.html')

def logout(request):
    response = HttpResponse('Logged out successfully!')
    response.delete_cookie('session_token')
    return redirect('flaws:login')

def user_pets(request, user_id):
    user = get_object_or_404(User, id=user_id)
    print("user id is", user_id)
    pets = Pet.objects.filter(owner=user)
    return render(request, 'user_pets.html', {'user': user, 'pets': pets})


def admin_view(request):
    session_token = request.COOKIES.get('session_token')
    if not session_token:
        return redirect('flaws:login')
    try:
        user = User.objects.get(session_token=session_token)
        if "admin" in user.username:
            user_list = User.objects.all()
            return render(request, 'admin_view.html', {'user_list': user_list})
        
    except User.DoesNotExist:
        return redirect('flaws:login')


class DetailView(generic.DetailView):
    model = Pet
    template_name = 'pet_details.html'


def admin_pets_query(request):
    pets = None
    if request.method == 'POST':
        id = request.POST.get('owner_id', 0)
        query = f"SELECT * FROM flaws_pet WHERE owner_id = {id}"

        with connection.cursor() as cursor:
            cursor.execute(query)
            pets = cursor.fetchall()
        return render(request, 'admin_petsearch.html', {'pet_list': pets, 'search_id': id})
    else:
        return render(request, 'admin_petsearch.html')


#def admin_pets_query(request):
#    pets = None
#    if request.method == 'POST':
#        id = request.POST.get('owner_id', 0)
#        pets = Pet.objects.filter(owner_id=id)
#        return render(request, 'admin_petsearch.html', {'pet_list': pets, 'search_id': id})
#    else:
#        return render(request, 'admin_petsearch.html')