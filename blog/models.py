from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import strip_tags
import math

from dominusoft.image_utils import compress_image_content


# Create your models here.
class Category_Article(models.Model):
    category_slug = models.SlugField(unique=True, null=True, blank=True)
    category_meta_keywords = models.CharField(max_length=300, null=True, blank=True)
    category_meta_descriptions = models.CharField(max_length=300, null=True, blank=True)
    category_title = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.category_slug}"
class Article(models.Model):
    article_slug = models.SlugField(unique=True, null=True, blank=True)
    article_created_at = models.DateTimeField(auto_now_add=True)
    artticle_meta_title = models.CharField(max_length=500, null=True, blank=True)
    article_author = models.CharField(max_length=300, null=True, blank=True)
    article_meta_keywords = models.CharField(max_length=300, null=True, blank=True)
    article_meta_descriptions = models.CharField(max_length=300, null=True, blank=True)
    article_title = models.CharField(max_length=500, null=True, blank=True)
    article_image = models.ImageField(upload_to="blog/")
    article_image_alt = models.CharField(max_length=300, null=True, blank=True)
    article_category = models.ForeignKey(
            Category_Article, on_delete=models.CASCADE, null=True, blank=True
        )
    article_excerpt = models.TextField(null=True, blank=True)
    article_infos = CKEditor5Field(
        "Article", config_name="extends", null=True, blank=True
    )

    @property
    def estimated_read_time(self):
        plain_text = strip_tags(self.article_infos or "")
        word_count = len(plain_text.split())
        return max(1, math.ceil(word_count / 200))

    def save(self, *args, **kwargs):
        if self.article_image:
            self.article_image = compress_image_content(self.article_image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.article_slug}"
