from django.contrib import admin
from django.urls import include, path
# 404
from django.conf.urls import handler404
from home.views import error_404
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", include("home.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("trajnime-profesionale/", include("trainings.urls")),
    # path("projektet-studentet/", include("student_project.urls")),
    # path("internshipe/", include("internship.urls")),
    path("sherbime-per-biznese/", include("services.urls")),
    path("apliko/", include("apply.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 404
# handler404 = error_404
handler404 = "home.views.error_404"