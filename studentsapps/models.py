from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.core.cache import cache
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from geopy.geocoders import Nominatim
import requests


class Student(models.Model):
    student_id = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    branch = models.CharField(max_length=55)
    # branch = models.CharField(max_length=55)
    
    def __str__(self):
        return self.name



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserLoginHistory(models.Model):
    """Model to track user login history with location and device information"""
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='login_history')
    login_datetime = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    device_type = models.CharField(max_length=255, blank=True)
    device_os = models.CharField(max_length=255, blank=True)
    browser = models.CharField(max_length=255, blank=True)
    location_city = models.CharField(max_length=255, blank=True)
    location_country = models.CharField(max_length=255, blank=True)
    is_suspicious = models.BooleanField(default=False)

    class Meta:
        ordering = ['-login_datetime']

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        unique=True,
        validators=[EmailValidator()],
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    
    password = models.CharField(
        _('password'),
        max_length=128,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                message=_('Password must contain at least 8 characters, including letters, numbers, and special characters.'),
            ),
        ]
    )

    # Personal information
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    # Status fields
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active.'),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    # Tracking fields
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), null=True, blank=True)
    
    # Security fields
    login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    
    # Login notification preferences
    notify_on_login = models.BooleanField(default=True)
    notify_on_suspicious_login = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def log_login(self, request, latitude=None, longitude=None):
        """
        Log a new login with device and location information
        """
        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # Get device info from user agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Create login history entry
        login_entry = UserLoginHistory.objects.create(
            user=self,
            ip_address=ip_address,
            latitude=latitude,
            longitude=longitude,
            device_type=self._get_device_type(user_agent),
            device_os=self._get_device_os(user_agent),
            browser=self._get_browser(user_agent)
        )

        # Send notification email if enabled
        if self.notify_on_login:
            self.send_login_notification(login_entry)

        return login_entry
    
    
    
    def _get_location_from_coordinates(self, latitude, longitude):
        if not latitude or not longitude:
            return None

        cache_key = f'location_data_{latitude}_{longitude}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
            
        try:
            geolocator = Nominatim(user_agent="studentsapps")
            location = geolocator.reverse(f"{latitude}, {longitude}", language="en")
            
            if location and location.raw.get('address'):
                address = location.raw['address']
                location_data = {
                    'city': address.get('city') or address.get('town') or address.get('suburb'),
                    'state': address.get('state'),
                    'country': address.get('country'),
                    'postal_code': address.get('postcode'),
                    'formatted_address': location.address,
                    'street': address.get('road'),
                    'district': address.get('district') or address.get('county'),
                    'region': address.get('region') or address.get('state')
                }
                cache.set(cache_key, location_data, 60 * 60 * 24)
                return location_data
                
        except Exception as e:
            print(f"Geocoding error: {str(e)}")
            
        return None

    def get_location_from_ip(self, ip_address):
        if ip_address == '127.0.0.1':
            return {
                'city': 'Local Development',
                'country': 'Development Environment',
                'latitude': None,
                'longitude': None
            }

        cache_key = f'ip_location_{ip_address}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
            
        try:
            response = requests.get(f'https://ipapi.co/{ip_address}/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                location_data = {
                    'city': data.get('city'),
                    'country': data.get('country_name'),
                    'region': data.get('region'),
                    'postal_code': data.get('postal'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                    'timezone': data.get('timezone'),
                    'org': data.get('org')
                }
                cache.set(cache_key, location_data, 60 * 60 * 24)
                return location_data
                
        except Exception as e:
            print(f"IP geolocation error: {str(e)}")
            
        return None
    
    
    
    

    def send_login_notification(self, login_entry):
        subject = f"Security Alert: New Login - {login_entry.login_datetime.strftime('%B %d, %Y')}"
        
        # Get detailed location
        location_data = None
        if login_entry.latitude and login_entry.longitude:
            location_data = self._get_location_from_coordinates(login_entry.latitude, login_entry.longitude)
        if not location_data:
            location_data = self.get_location_from_ip(login_entry.ip_address)
        
        context = {
            'user': self,
            'login_time': login_entry.login_datetime,
            'location_city': location_data.get('city') if location_data else None,
            'location_country': location_data.get('country') if location_data else None,
            'location_region': location_data.get('region') if location_data else None,
            'location_postal': location_data.get('postal_code') if location_data else None,
            'location_street': location_data.get('street') if location_data else None,
            'ip_address': login_entry.ip_address,
            'device_type': login_entry.device_type,
            'device_os': login_entry.device_os,
            'browser': login_entry.browser,
            'is_new_location': True,
            'site_name': 'StudentsApps',
            'timezone': location_data.get('timezone') if location_data else 'UTC',
            'site_url': settings.SITE_URL, 
            'support_email': settings.SUPPORT_EMAIL,  
        }
        
        email_html = render_to_string('emails/login_notification_email.html', context)
        email_text = strip_tags(email_html)
        
        send_mail(
            subject=subject,
            message=email_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            html_message=email_html,
            fail_silently=False
        )

    def _get_device_type(self, user_agent):
        """Extract device type from user agent"""
        if 'Mobile' in user_agent:
            return 'Mobile'
        elif 'Tablet' in user_agent:
            return 'Tablet'
        return 'Desktop'

    def _get_device_os(self, user_agent):
        """Extract OS from user agent"""
        os_list = ['Windows', 'Mac OS X', 'Linux', 'Android', 'iOS']
        for os in os_list:
            if os in user_agent:
                return os
        return 'Unknown'

    def _get_browser(self, user_agent):
        """Extract browser from user agent"""
        browsers = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera']
        for browser in browsers:
            if browser in user_agent:
                return browser
        return 'Unknown'

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def increment_login_attempts(self):
        self.login_attempts += 1
        if self.login_attempts >= 5:
            self.locked_until = timezone.now() + timezone.timedelta(hours=2)
        self.save()

    def reset_login_attempts(self):
        self.login_attempts = 0
        self.locked_until = None
        self.save()

    def is_locked(self):
        if self.locked_until and self.locked_until > timezone.now():
            return True
        return False