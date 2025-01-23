from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Student, UserLoginHistory

@admin.register(UserLoginHistory)
class UserLoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_datetime', 'ip_address', 'device_type', 'browser', 'location_city', 'is_suspicious')
    list_filter = ('device_type', 'browser', 'is_suspicious', 'login_datetime')
    search_fields = ('user__email', 'ip_address', 'location_city', 'location_country')
    readonly_fields = ('login_datetime', 'user', 'ip_address', 'latitude', 'longitude', 
                      'device_type', 'device_os', 'browser', 'location_city', 'location_country')
    
    fieldsets = (
        (_('User Info'), {'fields': ('user', 'login_datetime')}),
        (_('Location'), {'fields': ('ip_address', 'latitude', 'longitude', 'location_city', 'location_country')}),
        (_('Device Info'), {'fields': ('device_type', 'device_os', 'browser')}),
        (_('Security'), {'fields': ('is_suspicious',)}),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'notify_on_login', 'notify_on_suspicious_login')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                     'groups', 'user_permissions')}),
        (_('Security'), {'fields': ('login_attempts', 'locked_until', 
                                  'notify_on_login', 'notify_on_suspicious_login')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )

    readonly_fields = ('date_joined', 'last_login', 'login_attempts', 'locked_until')

    def get_inline_instances(self, request, obj=None):
        if obj:
            self.inlines = [UserLoginHistoryInline]
        return super().get_inline_instances(request, obj)

class UserLoginHistoryInline(admin.TabularInline):
    model = UserLoginHistory
    extra = 0
    can_delete = False
    readonly_fields = ('login_datetime', 'ip_address', 'device_type', 'browser', 
                      'location_city', 'location_country', 'is_suspicious')
    ordering = ('-login_datetime',)
    max_num = 5
    verbose_name = _("Recent Login History")
    verbose_name_plural = _("Recent Login History")

admin.site.register(Student)