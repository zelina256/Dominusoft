import re
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
    cat_training_icon = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default="fas fa-graduation-cap",
        help_text="P.sh. 'fas fa-code' ose 'fas fa-chart-line'",
    )
    cat_meta_keyword = models.CharField(max_length=500, null=True, blank=True)
    cat_meta_description = models.CharField(max_length=500, null=True, blank=True)
    cat_slug = models.SlugField(unique=True)
    cat_title_tag = models.CharField(max_length=300, null=True, blank=True)

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
    training_icon = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default="fas fa-laptop-code",
        help_text="P.sh. 'fab fa-python' ose 'fas fa-chart-line'",
    )
    training_category = models.ForeignKey(
        Category_training, on_delete=models.CASCADE, null=True
    )
    training_slug = models.SlugField(unique=True)
    training_meta_keywords = models.CharField(max_length=500, null=True, blank=True)
    training_meta_descriptions = models.CharField(max_length=500, null=True, blank=True)
    training_title_tag = models.CharField(max_length=300, null=True, blank=True)
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
        source_urls = [
            "https://iliria98.com/convert",
        ]

        for url in source_urls:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                text = response.text

                if "iliria98.com/convert" in url:
                    match = re.search(r"EUR\s*(\d{1,3}(?:[.,]\d{1,2})?)\s*(\d{1,3}(?:[.,]\d{1,2})?)", text)
                    if match:
                        first = Decimal(match.group(1).replace(",", "."))
                        second = Decimal(match.group(2).replace(",", "."))
                        return (first + second) / Decimal("2")

                data = response.json()
                if data.get("rates"):
                    all_per_eur = data.get("rates", {}).get("ALL")
                    if all_per_eur:
                        return Decimal(str(all_per_eur))

                    eur_per_all = data.get("rates", {}).get("EUR")
                    if eur_per_all:
                        return Decimal(str(1)) / Decimal(str(eur_per_all))
            except Exception:
                continue

        return Decimal("92.17")

    @property
    def training_price_eur(self):
        if self.training_price_lek is None:
            return Decimal("0.00")

        rate = self.get_lek_to_eur_rate()
        amount = Decimal(str(self.training_price_lek)) / rate
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
