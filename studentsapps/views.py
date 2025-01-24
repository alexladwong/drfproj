from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
import requests
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.conf import settings
from django.utils.html import strip_tags
from .models import CustomUser
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
  
from django.contrib.auth import logout


@login_required(login_url='login')
def home(request):
    students = [
        {'id': 1, 'name': 'Alexander Joshua Ladwong', 'age': 10},
        {'id': 2, 'name': 'Alexander Shepard Otim', 'age': 7},
        {'id': 3, 'name': 'Ladwong Alexander Chief', 'age': 2}
    ]
    
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse({
            'success': True,
            'students': students,
            'redirect_url': '/'
        })
    messages.success(request, 'Welcome Back {{username}}')
    return render(request, 'home.html', {'students': students})
  

@ensure_csrf_cookie
def get_location_from_ip(ip_address):
    """Get location details from IP address using ipapi.co"""
    try:
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        if response.status_code == 200:
            data = response.json()
            return {
                'city': data.get('city', ''),
                'country': data.get('country_name', ''),
                'latitude': data.get('latitude', None),
                'longitude': data.get('longitude', None)
            }
    except Exception as e:
        print(f"Error getting location data: {e}")
    return None
  
  
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

@ensure_csrf_cookie
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Basic validation
        if not all([email, password, password_confirm, first_name, last_name]):
            messages.error(request, 'All fields are required')
            return render(request, 'auth/register.html')

        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address')
            return render(request, 'auth/register.html')

        # Check if email already exists
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered')
            return render(request, 'auth/register.html')

        # Password validation
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return render(request, 'auth/register.html')

        # Password strength validation
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'auth/register.html')

        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            messages.error(request, 'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character')
            return render(request, 'auth/register.html')

        try:
            # Create new user
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            # Log the user in
            login(request, user)

            # Log the registration location
            login_entry = user.log_login(request, latitude, longitude)

            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': '/'
                })

            messages.success(request, 'Registration successful! Welcome to our platform.')
            return redirect('/')

        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
            messages.error(request, f'An error occurred during registration: {str(e)}')
            return render(request, 'auth/register.html')

    # GET request - display registration form
    return render(request, 'auth/register.html')
  
  


@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        if not email or not password:
            messages.error(request, 'Please provide both email and password')
            return render(request, 'auth/login.html')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Check if account is locked
            if user.is_locked():
                lock_time_remaining = user.locked_until - timezone.now()
                messages.error(
                    request, 
                    f'Account is locked. Please try again in {lock_time_remaining.seconds//60} minutes'
                )
                return render(request, 'auth/login.html')

            # Get IP and location data
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')

            # Initialize location_data
            location_data = None

            # If no coordinates provided by browser, try to get from IP
            if not latitude or not longitude:
                location_data = get_location_from_ip(ip_address)
                if location_data:
                    latitude = location_data['latitude']
                    longitude = location_data['longitude']

            # Log the login
            login_entry = user.log_login(request, latitude, longitude)

            # Update login history with location data if available
            if location_data:
                login_entry.location_city = location_data['city']
                login_entry.location_country = location_data['country']
                login_entry.save()

            # Reset login attempts on successful login
            user.reset_login_attempts()
            
            # Actually log the user in
            login(request, user)
            
            # Return JSON if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': '/'})
            
            return redirect('/')  # Redirect to home

        else:
            # Get user by email to increment login attempts
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                user.increment_login_attempts()
            except User.DoesNotExist:
                pass

            messages.error(request, 'Invalid email or password')
            return render(request, 'auth/login.html')

    return render(request, 'auth/login.html')
  
  

def password_reset_request(request):
    """
    Handle password reset request and send reset email
    """
    if request.method == "POST":
        email = request.POST.get('email', '')
        try:
            user = CustomUser.objects.get(email=email)
            
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create password reset link
            domain = request.get_host()
            protocol = 'https' if request.is_secure() else 'http'
            reset_url = f"{protocol}://{domain}/password-reset-confirm/{uid}/{token}/"
            
            # Prepare email content
            context = {
                'user': user,
                'reset_url': reset_url,
                'domain': domain,
                'site_name': 'Your Site Name',
                'uid': uid,
                'token': token,
                'protocol': protocol,
            }
            
            # Render email templates
            email_html_message = render_to_string('auth/password_reset_email.html', context)
            email_plaintext_message = strip_tags(email_html_message)
            
            try:
                # Send email
                send_mail(
                    subject="Password Reset Requested",
                    message=email_plaintext_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=email_html_message,
                    fail_silently=False,
                )
                messages.success(request, 
                    "Password reset instructions have been sent to your email.")
                return redirect('/login')
                
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            
        except CustomUser.DoesNotExist:
            messages.error(request, 
                "If an account exists with this email, you will receive password reset instructions.")
            # We return success even if email doesn't exist for security
            return redirect('login')
    
    return render(request, 'auth/password_reset_form.html')

def password_reset_confirm(request, uidb64, token):
    """
    Handle password reset confirmation and set new password
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if not password1 or not password2:
                messages.error(request, "Please enter both passwords.")
                return render(request, 'auth/password_reset_confirm.html')
                
            if password1 != password2:
                messages.error(request, "The passwords don't match.")
                return render(request, 'auth/password_reset_confirm.html')
            
            try:
                password_validation.validate_password(password1, user)
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
                return render(request, 'auth/password_reset_confirm.html')
            
            user.set_password(password1)
            user.login_attempts = 0
            user.locked_until = None
            user.save()
            
            # Log the user in after password reset
            login(request, user)
            
            messages.success(request, "Your password has been reset successfully.")
            return redirect('/')  # Redirect to home
            
        return render(request, 'auth/password_reset_confirm.html')
    else:
        messages.error(request, 
            "The password reset link is invalid or has expired. Please request a new one.")
        return redirect('auth/password_reset_request')


def password_change(request):
    """
    Handle password change for logged-in users
    """
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if not request.user.check_password(old_password):
            messages.error(request, "Your old password was entered incorrectly.")
            return render(request, 'auth/password_change.html')
            
        if new_password1 != new_password2:
            messages.error(request, "The new passwords don't match.")
            return render(request, 'auth/password_change.html')
            
        try:
            password_validation.validate_password(new_password1, request.user)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, 'auth/password_change.html')
            
        request.user.set_password(new_password1)
        request.user.save()
        
        update_session_auth_hash(request, request.user)
        messages.success(request, "Your password was successfully changed.")
        return redirect('/')  # Redirect to home
        
    return render(request, 'auth/password_change.html')
  
  
  
# def TwoFactors(request):
#   return
  
  


def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')