from django.db import models

# Create your models here.
# Partneret
class Partner(models.Model):
    partner_id = models.AutoField(primary_key=True)
    partner_name = models.CharField(max_length=250, null=True, blank=True)
    partner_logo = models.ImageField(
        upload_to="static/images/partner", null=True, blank=True
    )
    partner_image_alt = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.partner_name}"
