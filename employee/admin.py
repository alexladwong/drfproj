from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'emp_name', 'email', 'emp_phone_number', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('emp_name', 'email', 'emp_phone_number')
    list_filter = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('emp_id', 'emp_name', 'email', 'emp_phone_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
