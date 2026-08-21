from decimal import Decimal, InvalidOperation

import requests
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.safestring import mark_safe


# Create your models here.
# Kategoria e trajnimeve
class Category_training(models.Model):
    cat_training_id = models.AutoField(primary_key=True)
    cat_training_name = models.CharField(max_length=100, null=True)
    cat_training_text_short = models.TextField(max_length=200, null=True)
    cat_training_text_description = models.TextField(null=True)
    cat_training_img = models.ImageField(upload_to="static/images/training", null=True)
    cat_training_img_alt = models.CharField(max_length=50, null=True)
    cat_meta_keyword = models.CharField(max_length=200, null=True)
    cat_meta_description = models.CharField(max_length=300, null=True)
    cat_slug = models.SlugField(unique=True)
    cat_title_tag = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.cat_training_name}"

    @property
    def get_training(self):
        return Training.objects.filter(
            training_category__cat_training_name=self.cat_training_name
        )


# Trajnimet te grupuara ne kategori


class Training(models.Model):
    training_id = models.AutoField(primary_key=True)
    training_name = models.CharField(max_length=30, null=True)
    training_text = models.TextField(null=True)
    training_employment = CKEditor5Field(
        "Text", config_name="extends", null=True, blank=True
    )
    training_sessions = models.CharField(max_length=30, null=True)
    training_hours = models.IntegerField(null=True)
    training_weeks = models.IntegerField(null=True)
    training_competence = CKEditor5Field(
        "Text", config_name="extends", null=True, blank=True
    )
    training_image = models.ImageField(upload_to="static/images/training", null=True)
    training_image_alt = models.CharField(max_length=50, null=True)
    training_category = models.ForeignKey(
        Category_training, on_delete=models.CASCADE, null=True
    )
    training_slug = models.SlugField(unique=True)
    training_meta_keywords = models.CharField(max_length=300, null=True)
    training_meta_descriptions = models.CharField(max_length=300, null=True)
    training_title_tag = models.CharField(max_length=200, null=True)
    training_price_lek = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        blank=True,
        null=True,
        help_text="Çmimi në lekë, i futur manualisht."
    )

    @staticmethod
    def get_lek_to_eur_rate():
        try:
            response = requests.get(
                "https://api.exchangerate.host/latest?base=ALL&symbols=EUR",
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()
            rate = data.get("rates", {}).get("EUR")
            if rate:
                return Decimal(str(rate))
        except Exception:
            pass

        return Decimal("0.0082")

    @property
    def training_price_eur(self):
        if self.training_price_lek is None:
            return Decimal("0.00")

        rate = self.get_lek_to_eur_rate()
        amount = Decimal(str(self.training_price_lek)) * rate
        return amount.quantize(Decimal("0.01"))

    def __str__(self):
        return f"{self.training_name}"


# Projektet qe mund te ndertohen gjate trajnimeve
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100, null=True)
    project_training = models.ManyToManyField(Training)

    def __str__(self):
        return f"{self.project_name}"


# Karriera qe mund te ndiqet
class Career(models.Model):
    career_id = models.AutoField(primary_key=True)
    career_opportunity = models.CharField(max_length=100, null=True)
    career_training = models.ManyToManyField(Training)

    def __str__(self):
        return f"{self.career_opportunity}"


# Kurrikula
class Curricula(models.Model):
    curricula_id = models.AutoField(primary_key=True)
    curricula_name = models.CharField(max_length=250, null=True)
    curricula_train = models.ManyToManyField(Training)

    def __str__(self):
        return f"{self.curricula_name}"

    @property
    def get_lesson(self):
        return Lesson.objects.filter(
            lesson_curricula__curricula_name=self.curricula_name
        )


# Temat
class Lesson(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    lesson_name = models.CharField(max_length=2000, null=True)
    lesson_curricula = models.ForeignKey(Curricula, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.lesson_name}"
