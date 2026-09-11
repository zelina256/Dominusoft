from django.db import models
from trainings.models import Training
from services.models import Services


# Create your models here.
# Form Kursant
class Student(models.Model):
    class UniversityDegreeChoices(models.TextChoices):
        ARSIM_9_VJEC = "arsim_9_vjec", "Arsim 9-vjeçar"
        GJIMNAZPERGJITHSHEM = "gjimnaz_pergjithshem", "Gjimnaz i Përgjithshëm"
        GJIMNAZPROFESIONAL = "gjimnaz_profesional", "Gjimnaz Profesional"
        BACHELOR = "bachelor", "Bachelor"
        MASTERPROFESIONAL = "master_profesional", "Master Profesional"
        MASTERSHENCOR = "master_shencor", "Master Shkencor"
    
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=50, null=True, blank=True)
    student_surname = models.CharField(max_length=50, null=True, blank=True)
    student_father_name = models.CharField(max_length=100, null=True, blank=True)
    student_birthday = models.DateField(null=True, blank=True)
    student_email = models.EmailField(max_length=254, null=True, blank=True)
    student_phone = models.CharField(max_length=50, null=False, blank=False)
    student_card_id_number = models.CharField(max_length=20, null=True, blank=True)
    student_university_degree = models.CharField(
        max_length=20,
        choices=UniversityDegreeChoices.choices,
        null=True,
        blank=True,
    )
    student_training = models.ForeignKey(Training, on_delete=models.CASCADE, null=True, blank=True)
    student_timetable = models.CharField(max_length=20, null=True, blank=True)
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

    
    
class Contact(models.Model):
    submission_token = models.CharField(max_length=32, unique=True)
    contact_name = models.CharField(max_length=50, null=True, blank=True)
    contact_surname = models.CharField(max_length=50, null=True, blank=True)
    contact_email = models.EmailField(max_length=254, null=True, blank=True)
    contact_phone = models.CharField(max_length=50, null=False, blank=False)
    contact_subject = models.CharField(max_length=200, null=True, blank=True)
    contact_message = models.TextField(max_length=1000, null=True, blank=True)
    submit_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.contact_name} {self.contact_surname} - {self.contact_subject}"
    
class Subscribe(models.Model):
    subscribe_id = models.AutoField(primary_key=True)
    subscribe_email = models.EmailField(max_length=254, null=True, unique=True)
    submit_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.subscribe_id} - {self.subscribe_email}"