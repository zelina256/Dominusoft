from django.db import models
from trainings.models import Training
from services.models import Services


# Create your models here.
# Form Kursant
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=50, null=True, blank=True)
    student_surname = models.CharField(max_length=50, null=True, blank=True)
    student_email = models.EmailField(max_length=254, null=True, blank=True)
    student_phone = models.CharField(max_length=50, null=False, blank=False)
    student_training = models.ForeignKey(Training, on_delete=models.CASCADE, null=True, blank=True)
    student_terms_accepted = models.BooleanField(default=False)
    student_message = models.TextField(max_length=300, null=True, blank=True)
    submission_token = models.CharField(max_length=32, unique=True)
    submit_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f"{self.student_name} {self.student_surname} - {self.student_training}"

# Form Biznes
class Business(models.Model):
    business_id = models.AutoField(primary_key=True)
    submission_token = models.CharField(max_length=32, unique=True)
    business_name = models.CharField(max_length=100, null=True, blank=True)
    business_delegate = models.CharField(max_length=100, null=True, blank=True)
    business_email = models.EmailField(max_length=254, null=True, blank=True)
    business_phone = models.CharField(max_length=50, null=False, blank=False)
    business_service = models.ForeignKey(Services, on_delete=models.CASCADE, null=True, blank=True)
    business_message = models.TextField(max_length=300, null=True, blank=True)
    submit_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return f"{self.business_name} - {self.business_service}"

    
class Subscribe(models.Model):
    subscribe_id = models.AutoField(primary_key=True)
    subscribe_email = models.EmailField(max_length=254, null=True, unique=True)
    submit_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.subscribe_id} - {self.subscribe_email}"