from django.db import models
from trainings.models import *

# Create your models here.

# Kategori Projekti te Kursanteve
class Student_Project_Category(models.Model):
    student_project_category_id = models.AutoField(primary_key=True)
    student_project_category_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.student_project_category_name}"
    
    @property
    def get_studentproject(self):
        return Student_work.objects.filter(student_project_training_category__student_project_category_name=self.student_project_category_name).order_by('student_project_id')[::-1]

# Projekti - Kursant
class Student_work(models.Model):
    student_project_id = models.AutoField(primary_key=True)
    student_project_name = models.CharField(max_length=50, null=True)
    student_project_surname = models.CharField(max_length=50, null=True)
    student_project_text = models.TextField(max_length=450, null=True)
    student_project_image = models.ImageField(upload_to='static/images/student', null=True)
    student_project_gif = models.ImageField(upload_to='static/images/student', null=True)
    student_project_training = models.CharField(max_length=100, null=True)
    student_project_training_category = models.ForeignKey(Student_Project_Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.student_project_name} {self.student_project_surname}"
