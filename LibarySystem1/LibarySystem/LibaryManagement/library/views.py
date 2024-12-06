from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm
from .models import User

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.access_level = 'user'  # Thiết lập quyền truy cập mặc định là 'user'
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Authentication failed.')
        else:
            messages.error(request, 'Form is not valid.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username2']
        password = request.POST['password2']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Kiểm tra trường hợp đặc biệt cho tài khoản admin
            if user.username == 'admin' and password == '1234567890':
                user.access_level = 'admin'  # Đảm bảo quyền admin
                user.save(update_fields=['access_level'])  # Cập nhật quyền truy cập nếu cần

            login(request, user)
            if user.access_level == 'admin':
                return redirect('admin_custom')
            elif user.access_level == 'content manager':
                return redirect('dashboard_content_manager')
            else:
                return redirect('dashboard_user')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

@login_required
def custom_admin(request):
    # Kiểm tra tài khoản admin đặc biệt
    if request.user.username == 'admin' and request.user.check_password('1234567890'):
        users = User.objects.all()
        return render(request, 'adminControl.html', {'users': users})

    # Kiểm tra quyền truy cập thông thường
    if request.user.access_level != 'admin':
        messages.error(request, 'Access denied')
        return redirect('home')

    users = User.objects.all()
    return render(request, 'adminControl.html', {'users': users})

@login_required
def dashboard_user(request):
    return render(request, 'dashboard_user.html')

@login_required
def dashboard_content_manager(request):
    return render(request, 'dashboard_content_manage.html')

@login_required
def admin(request):
    # Kiểm tra tài khoản admin đặc biệt
    if request.user.username == 'admin' and request.user.check_password('1234567890'):
        users = User.objects.all()
        return render(request, 'adminControl.html', {'users': users})

    # Kiểm tra quyền thông thường
    if request.user.access_level != 'admin':
        messages.error(request, 'Access denied')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        role = request.POST['role']
        if username and password and email and role:
            User.objects.create_user(username=username, password=password, email=email, access_level=role)
            messages.success(request, 'User added successfully')
        else:
            messages.error(request, 'Invalid input')

    users = User.objects.all()
    return render(request, 'adminControl.html', {'users': users})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def edit_role(request, id):
    if request.user.access_level == 'admin':
        user = User.objects.get(id=id)
        new_role = request.POST['role']
        user.access_level = new_role
        user.save()
        return redirect('admin_custom')
    else:
        messages.error(request, 'Access denied')
        return redirect('home')

@login_required
def delete_user(request, id):
    if request.user.access_level == 'admin':
        user = User.objects.get(id=id)
        user.delete()
        return redirect('admin_custom')
    else:
        messages.error(request, 'Access denied')
        return redirect('home')

@login_required
def add_user_route(request):
    if request.user.access_level == 'admin':
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            role = request.POST['role']
            if username and password and email and role:
                User.objects.create_user(username=username, password=password, email=email, access_level=role)
                messages.success(request, 'User added successfully')
                return redirect('admin_custom')
            else:
                messages.error(request, 'Invalid input')
        users = User.objects.all()
        return render(request, 'adminControl.html', {'users': users})
    else:
        messages.error(request, 'Access denied')
        return redirect('home')
