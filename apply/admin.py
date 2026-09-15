from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_name",
        "student_surname",
        "student_email",
        "student_phone",
        "student_training",
        "submit_at",
    )
    search_fields = ("student_name", "student_surname", "student_training", "submit_at")

# admin.site.register(Business)
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = (
        "business_name",
        "business_delegate",
        "business_email",
        "business_phone",
        "business_service",
    )
    search_fields = ("business_name", "business_delegate", "business_service", "submit_at")

    
@admin.register(Subscribe)
class Subscribe(admin.ModelAdmin):
    list_display = ("subscribe_id", "subscribe_email", "submit_at")
    search_fields = ("subscribe_email", "submit_at")

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "contact_name",
        "contact_surname",
        "contact_email",
        "contact_phone",
        "contact_subject",
        "contact_message",
        "submit_at",
    )
    search_fields = ("contact_name", "contact_surname", "contact_email", "contact_subject", "submit_at")