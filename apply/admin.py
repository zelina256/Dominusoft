from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_name", "student_surname", "student_training", "submit_at")
    search_fields = ("student_name", "student_surname", "student_training", "submit_at")

# admin.site.register(Business)
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ("business_name", "business_delegate", "business_service", "submit_at")
    search_fields = ("business_name", "business_delegate", "business_service", "submit_at")

# admin.site.register(NewStaff)
@admin.register(NewStaff)
class NewStaffAdmin(admin.ModelAdmin):
    list_display = ("staff_name", "staff_surname", "staff_position", "submit_at")
    search_fields = ("staff_name", "staff_surname", "staff_position", "submit_at")
    
@admin.register(Subscribe)
class Subscribe(admin.ModelAdmin):
    list_display = ("subscribe_email", "submit_at")
    search_fields = ("subscribe_email", "submit_at")
