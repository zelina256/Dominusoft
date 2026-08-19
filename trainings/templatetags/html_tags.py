from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter(name='html_tags')
def html_tags(value):
    return mark_safe(value)


@register.filter(name='article_category_label')
def article_category_label(article):
  
    if not article or not getattr(article, "article_category", None):
        return "Pa kategori"

    category = article.article_category
    return category.category_title or category.category_slug or "Pa kategori"
