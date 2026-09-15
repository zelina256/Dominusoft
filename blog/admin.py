from datetime import timedelta

from django.contrib import admin
from django.utils import timezone

from .models import Article, Category_Article


@admin.register(Category_Article)
class CategoryArticleAdmin(admin.ModelAdmin):
    list_display = (
        "category_title",
    )
    search_fields = ("category_title", "category_slug", "category_meta_keywords")
    prepopulated_fields = {"category_slug": ("category_title",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "article_title",
        "article_created_at",
        "article_publish_at",
        "article_status",
        "article_category",
        "article_created_at",
    )
    search_fields = ("article_title", "article_slug", "article_meta_keywords")
    list_filter = ("article_category", "article_status", "article_publish_at")
    prepopulated_fields = {"article_slug": ("article_title",)}
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "article_title",
                    "article_slug",
                    "article_status",
                    "article_publish_at",
                    "article_category",
                    "article_author",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "artticle_meta_title",
                    "article_meta_keywords",
                    "article_meta_descriptions",
                )
            },
        ),
        (
            "Content",
            {
                "fields": (
                    "article_image",
                    "article_image_alt",
                    "article_excerpt",
                    "article_infos",
                )
            },
        ),
    )

    @admin.display(description="Read Time")
    def read_time_display(self, obj):
        return f"{obj.estimated_read_time} min"

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("-article_created_at", "-id")

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field=from_field)
        if obj and obj.article_image and not obj.article_image.storage.exists(obj.article_image.name):
            obj.article_image = None
            obj.save(update_fields=["article_image"])
        return obj

    def save_model(self, request, obj, form, change):
        if obj.article_status == Article.ArticleStatus.DRAFT:
            obj.article_publish_at = None
        elif obj.article_status == Article.ArticleStatus.PUBLISHED and not obj.article_publish_at:
            obj.article_publish_at = timezone.now()
        elif obj.article_status == Article.ArticleStatus.SCHEDULED and not obj.article_publish_at:
            obj.article_publish_at = timezone.now() + timedelta(hours=1)
        obj.clear_missing_image()
        super().save_model(request, obj, form, change)

    actions = ["make_draft", "make_published", "schedule_for_next_hour"]

    @admin.action(description="Mark selected as draft")
    def make_draft(self, request, queryset):
        queryset.update(article_status=Article.ArticleStatus.DRAFT, article_publish_at=None)

    @admin.action(description="Publish selected immediately")
    def make_published(self, request, queryset):
        queryset.update(
            article_status=Article.ArticleStatus.PUBLISHED,
            article_publish_at=timezone.now(),
        )

    @admin.action(description="Schedule selected for 1 hour from now")
    def schedule_for_next_hour(self, request, queryset):
        queryset.update(
            article_status=Article.ArticleStatus.SCHEDULED,
            article_publish_at=timezone.now() + timedelta(hours=1),
        )
