"""dominusoft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from .sitemaps import (
    ArticleSitemap,
    ServiceSitemap,
    StaticViewSitemap,
    TrainingCategorySitemap,
    TrainingSitemap,
)

# 404
from django.conf.urls import handler404
from home.views import error_404, robots_txt
from django.conf.urls.static import static
from django.conf import settings

sitemaps = {
    "static": StaticViewSitemap(),
    "training-categories": TrainingCategorySitemap(),
    "trainings": TrainingSitemap(),
    "articles": ArticleSitemap(),
    "services": ServiceSitemap()
}

urlpatterns = [
    path("robots.txt", robots_txt, name="robots_txt"),
    path("", include("home.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("kurse/", include("trainings.urls")),
    path("sherbime/", include("services.urls")),
    path("blog/", include("blog.urls")),
    path("apliko/", include("apply.urls")),
    path("dom-21/", admin.site.urls),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [path("<path:unmatched_path>", error_404)]

# 404
# handler404 = error_404
handler404 = "home.views.error_404"
