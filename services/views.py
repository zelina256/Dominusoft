from django.shortcuts import get_object_or_404, render

from trainings.models import Category_training

from .models import Services


# Sherbimet
def services(request):
    cat_trainings = Category_training.objects.all().order_by("cat_training_id")
    services = (
        Services.objects
        .select_related("detail")
        .prefetch_related("highlights", "benefits", "packages__items")
        .all()
        .order_by("-pk")
    )
    context = {"cat_trainings": cat_trainings, "services": services}
    return render(request, "sherbime/sherbime.html", context)


def tech_services(request, slug):
    service = get_object_or_404(
        Services.objects.prefetch_related(
            "highlights",
            "benefits",
            "packages__items",
            "offerings",
            "projects",
        ),
        slug=slug,
    )

    detail = None
    try:
        detail = service.detail
    except Services.detail.RelatedObjectDoesNotExist:
        detail = None

    context = {
        "service": service,
        "detail": detail,
        "highlights": service.highlights.all(),
        "benefits": service.benefits.all(),
        "packages": service.packages.all(),
        "offerings": service.offerings.all(),
        "projects": service.projects.filter(is_published=True),
        "faqs": [],
        "related_services": [],
    }
    return render(request, "sherbime/detaje_sherbime.html", context)