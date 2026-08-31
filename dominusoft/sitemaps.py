from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Article
from trainings.models import Category_training, Training


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return [
            "home",
            "training_category",
            "services",
            "blog",
            "student",
            "business",
            "career",
        ]

    def location(self, item):
        return reverse(item)


class TrainingCategorySitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return Category_training.objects.exclude(cat_slug="").order_by("pk")

    def location(self, item):
        return reverse("trainings", args=[item.cat_slug])


class TrainingSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return Training.objects.select_related("training_category").exclude(
            training_slug=""
        ).exclude(training_category__cat_slug="").order_by("pk")

    def location(self, item):
        return reverse(
            "curricula",
            args=[item.training_category.cat_slug, item.training_slug],
        )


class ArticleSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        return Article.objects.exclude(article_slug__isnull=True).exclude(
            article_slug=""
        ).order_by("pk")

    def lastmod(self, item):
        return item.article_created_at

    def location(self, item):
        return reverse("article", args=[item.article_slug])
