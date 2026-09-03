from django.shortcuts import get_object_or_404, redirect, render
from trainings.models import Category_training
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.


def blog(request):
    categories = Category_Article.objects.all().order_by("category_title")
    cat_trainings = Category_training.objects.all()
    selected_category = request.GET.get("category")
    raw_search_query = request.GET.get("q")
    search_query = (raw_search_query or "").strip()
    if raw_search_query is not None and not search_query:
        return redirect(request.path)
    articles = Article.published_objects.all().order_by("-article_created_at", "-id")
    if selected_category:
        articles = articles.filter(
            article_category__category_slug=selected_category
        )
    if search_query:
        articles = articles.filter(
            Q(article_title__icontains=search_query)
            | Q(article_infos__icontains=search_query)
        )

    paginator = Paginator(articles, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "articles": articles,
        "page_obj": page_obj,
        "categories": categories,
        "selected_category": selected_category,
        "search_query": search_query,
        "cat_trainings": cat_trainings
    }
    return render(request, "blog/blog.html", context)


def article(request, slug):
    articleInfo = get_object_or_404(
        Article.published_objects.select_related("article_category"), article_slug=slug
    )
    cat_trainings = Category_training.objects.all()
    articles = Article.published_objects.select_related("article_category").exclude(
        pk=articleInfo.pk
    ).order_by("-article_created_at", "-id")
    related_articles = articles.filter(
        article_category=articleInfo.article_category
    )[:3]
    if not related_articles:
        related_articles = articles[:3]
    context = {
        "articleInfo": articleInfo,
        "articles": articles,
        "same_training": related_articles,
        "cat_trainings": cat_trainings,
    }
    return render(request, "blog/article.html", context)
