from django.db import models

# Create your models here.

# Sherbim
class Services(models.Model):
    services_id = models.AutoField(primary_key=True)
    services_slug = models.SlugField(max_length=100, unique=True, null=True)
    services_name = models.CharField(max_length=100, null=True)
    services_description = models.TextField(max_length=1000, null=True)
    services_image = models.ImageField(upload_to='static/images/services', null=True)
    services_alt = models.CharField(max_length=100, null=True)
    services_meta_keyword = models.CharField(max_length=250, null=True)
    services_meta_description = models.CharField(max_length=250, null=True)
    services_title = models.CharField(max_length=250, null=True)

    def __str__(self):
        return f"{self.services_name}"
