from django.db import models

# Create your models here.

# Kategori Internship
class Internship_Category(models.Model):
    internship_category_id = models.AutoField(primary_key=True)
    internship_category_name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return f"{self.internship_category_name}"
    
    @property
    def get_internship(self):
        return Internship.objects.filter(internship_project_category__internship_category_name=self.internship_category_name).order_by('internship_project_id')[::-1]


# Internship
class Internship(models.Model):
    internship_project_id = models.AutoField(primary_key=True)
    internship_project_title = models.CharField(max_length=100, null=True)
    internship_project_text = models.TextField(max_length=1000, null=True)
    internship_project_image = models.ImageField(upload_to='static/images/internship', null=True)
    internship_project_gif = models.ImageField(upload_to='static/images/internship', null=True)
    internship_project_category= models.ForeignKey(Internship_Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.internship_project_title}"