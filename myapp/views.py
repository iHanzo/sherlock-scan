from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from .models import RequestLog

def home(request):
    return render(request, 'myapp/home.html')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'myapp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        # Log request headers
        request_log = RequestLog.objects.create(
            user_agent=request.headers.get('User-Agent'),
            client_ip=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')),
            accept=request.headers.get('Accept'),
            accept_encoding=request.headers.get('Accept-Encoding'),
            accept_language=request.headers.get('Accept-Language'),
            connection=request.headers.get('Connection'),
            host=request.headers.get('Host'),
            referer=request.headers.get('Referer'),
            successful_login=False  # Initially set to False, update based on actual login result
        )
        request_log.save()

        # Process login attempt
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful.')
            request_log.successful_login = True  # Update request log if login successful
            request_log.save()
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

            # Update request log for unsuccessful login attempt
            request_log.save()  # Save the log with unsuccessful login attempt

    return render(request, 'myapp/login.html')
