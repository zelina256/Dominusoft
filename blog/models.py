import math

from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags
from django_ckeditor_5.fields import CKEditor5Field

from dominusoft.image_utils import compress_image_content


# Create your models here.
class Category_Article(models.Model):
    category_slug = models.SlugField(unique=True, null=True, blank=True)
    category_meta_keywords = models.CharField(max_length=300, null=True, blank=True)
    category_meta_descriptions = models.CharField(max_length=300, null=True, blank=True)
    category_title = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.category_slug}"


class PublishedArticleManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return (
            super()
            .get_queryset()
            .filter(
                models.Q(article_status=Article.ArticleStatus.PUBLISHED)
                | models.Q(
                    article_status=Article.ArticleStatus.SCHEDULED,
                    article_publish_at__lte=now,
                )
            )
        )


class Article(models.Model):
    class ArticleStatus(models.TextChoices):
        PUBLISHED = "published", "Published"
        SCHEDULED = "scheduled", "Scheduled"
        DRAFT = "draft", "Draft"

    article_slug = models.SlugField(unique=True, null=True, blank=True)
    article_created_at = models.DateTimeField(auto_now_add=True)
    article_publish_at = models.DateTimeField(null=True, blank=True)
    article_status = models.CharField(
        max_length=20,
        choices=ArticleStatus.choices,
        default=ArticleStatus.PUBLISHED,
    )
    artticle_meta_title = models.CharField(max_length=500, null=True, blank=True)
    article_author = models.CharField(max_length=300, null=True, blank=True)
    article_meta_keywords = models.CharField(max_length=300, null=True, blank=True)
    article_meta_descriptions = models.CharField(max_length=300, null=True, blank=True)
    article_title = models.CharField(max_length=500, null=True, blank=True)
    article_image = models.ImageField(upload_to="blog/", null=True, blank=True)
    article_image_alt = models.CharField(max_length=300, null=True, blank=True)
    article_category = models.ForeignKey(
        Category_Article, on_delete=models.CASCADE, null=True, blank=True
    )
    article_excerpt = models.TextField(null=True, blank=True)
    article_infos = CKEditor5Field(
        "Article", config_name="extends", null=True, blank=True
    )

    objects = models.Manager()
    published_objects = PublishedArticleManager()

    @property
    def is_published(self):
        if self.article_status == self.ArticleStatus.PUBLISHED:
            return True
        if self.article_status == self.ArticleStatus.SCHEDULED:
            return bool(self.article_publish_at and self.article_publish_at <= timezone.now())
        return False

    @property
    def estimated_read_time(self):
        plain_text = strip_tags(self.article_infos or "")
        word_count = len(plain_text.split())
        return max(1, math.ceil(word_count / 200))

    def clear_missing_image(self):
        if self.article_image and hasattr(self.article_image, "storage"):
            try:
                if not self.article_image.storage.exists(self.article_image.name):
                    self.article_image = None
                    return True
            except Exception:
                return False
        return False

    def save(self, *args, **kwargs):
        if self.article_status == self.ArticleStatus.PUBLISHED and not self.article_publish_at:
            self.article_publish_at = timezone.now()
        elif self.article_status == self.ArticleStatus.DRAFT:
            self.article_publish_at = None
        self.clear_missing_image()
        if self.article_image:
            self.article_image = compress_image_content(self.article_image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.article_slug}"
