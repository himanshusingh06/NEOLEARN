from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import EmailMessage 
from django.conf import settings
from .models import ContactMessage
def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Check if username or email already exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists!")
            return redirect('login')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('login')
        elif pass1 != pass2:
            messages.error(request, "Your password and confirm password are not the same!")
            return redirect('login')
        else:
            # Create new user
            my_user = User(username=uname, email=email, first_name=first_name, last_name=last_name)
            my_user.set_password(pass1)  # Use set_password() to properly hash the password
            my_user.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        # Authenticate user
        user = authenticate(request, username=username, password=password)

        # Check if user exists
        if user is None:
            messages.error(request, "Invalid UserName or Password.")
        else:
            # User exists, check password
            if user.check_password(password):
                # Password is correct, log in user
                auth.login(request, user)
                return redirect('home')
            else:
                # Incorrect password
                messages.error(request, "Invalid UserName or Password.")


    return render(request, 'login.html')

# Logout view
def logout(request):
    auth.logout(request)
    return redirect('home')

# Home view
def home(request):
    user = request.user if request.user.is_authenticated else None
    return render(request, 'landing.html', {'user': user})


def send_mail_to_admin(user_name, user_email, mobile_number,subject,user_message):
    
    message_body = f'Form filled by {user_name}--- with the email {user_email}.\n\nMobile number -- {mobile_number}\n\nThe Message provided is :\n {user_message}'
    message = EmailMessage(
        subject=f'New form filled by {user_name}--- with subject {subject}',
        body=message_body,
        from_email=settings.EMAIL_HOST_USER,
        to=['himanshusinghwork365@gmail.com']
    )
    message.send()


def contact(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        subject = request.POST.get('subject')
        user_message = request.POST.get('message')
        
        
        # Save the message to the database
        ContactMessage.objects.create(
            user_name=user_name,
            user_email=user_email,
            mobile_number=mobile_number,
            subject=subject,
            user_message=user_message
        )
        
        send_mail_to_admin(user_name, user_email, mobile_number, subject, user_message)
        return redirect('home')
    else:
        return render(request, 'contact.html')