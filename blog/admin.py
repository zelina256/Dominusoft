from django.contrib import admin
from .models import Article, Category_Article


@admin.register(Category_Article)
class CategoryArticleAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"category_title",
		"category_slug",
		"category_meta_keywords",
		"category_meta_descriptions",
	)
	search_fields = ("category_title", "category_slug", "category_meta_keywords")
	prepopulated_fields = {"category_slug": ("category_title",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"article_title",
		"article_slug",
		"article_category",
		"article_created_at",
		"read_time_display",
		"article_image",
	)
	search_fields = ("article_title", "article_slug", "article_meta_keywords")
	list_filter = ("article_category", "article_created_at")
	prepopulated_fields = {"article_slug": ("article_title",)}

	@admin.display(description="Read Time")
	def read_time_display(self, obj):
		return f"{obj.estimated_read_time} min"