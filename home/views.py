from urllib.parse import urlencode

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from .models import *
from trainings.models import *
from blog.models import Article

# from contact.models import *
from apply.models import *


# Search
def searchvenues(request):
    cat_trainings = Category_training.objects.all()
    if request.method == "POST":
        legacy_query = (request.POST.get("search") or request.POST.get("q") or "").strip()
        search_url = reverse("searchvenues")
        if legacy_query:
            search_url = f"{search_url}?{urlencode({'q': legacy_query})}"
        return redirect(search_url)

    searched = (request.GET.get("q") or "").strip()
    venues = Training.objects.none()
    if searched:
        venues = Training.objects.filter(
            Q(training_name__icontains=searched)
            | Q(training_text__icontains=searched)
            | Q(training_category__cat_training_name__icontains=searched)
        ).select_related("training_category").distinct()

    context = {
        "cat_trainings": cat_trainings,
        "searched": searched,
        "venues": venues,
    }
    return render(request, "search/search.html", context)


@require_POST
def subscribe(request):
    email = (request.POST.get("subscribe_email") or "").strip().lower()
    try:
        validate_email(email)
    except ValidationError:
        messages.error(
            request,
            "Ju lutemi vendosni një adresë email-i të vlefshme.",
            extra_tags="subscribe",
        )
    else:
        if Subscribe.objects.filter(subscribe_email__iexact=email).exists():
            messages.warning(
                request,
                "Kjo adresë është abonuar më parë. Faleminderit!",
                extra_tags="subscribe",
            )
        else:
            Subscribe.objects.create(subscribe_email=email)
            messages.success(
                request,
                "U abonuat me sukses. Mirë se erdhët!",
                extra_tags="subscribe",
            )

    next_target = (request.POST.get("next") or "").strip()
    if not url_has_allowed_host_and_scheme(
        next_target,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_target = reverse("home")
    next_target = next_target.split("#", 1)[0]
    return redirect(f"{next_target}#subscribe")


def robots_txt(request):
    content = "\n".join(
        [
            "User-agent: *",
            "Disallow: /dom-21/",
            "Disallow: /ckeditor5/",
            "Sitemap: https://dominusoft.al/sitemap.xml",
        ]
    )
    return HttpResponse(content, content_type="text/plain; charset=utf-8")


# Kryefaqja
def home(request):
    partners = Partner.objects.all()
    cat_trainings = Category_training.objects.all()
    latest_articles = Article.objects.select_related("article_category").order_by(
        "-article_created_at", "-id"
    )[:3]

    # Subscribe
    if request.method == "POST":
        if request.POST.get("subscribe_email"):
            email = request.POST.get("subscribe_email")
            subscribe = Subscribe()
            subscribe.subscribe_email = request.POST.get("subscribe_email")
            if Subscribe.objects.filter(subscribe_email=email).exists():
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Ju jeni bërë subscribe më parë në faqen tonë. Faleminderit !",
                    extra_tags="subscribe",
                )
            else:
                subscribe.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Ju tashmë jeni pjesë e jona!",
                    extra_tags="subscribe",
                )
    context = {
        "partners": partners,
        "cat_trainings": cat_trainings,
        "latest_articles": latest_articles,
    }
    return render(request, "kryefaqja/kryefaqja.html", context)


# Rreth Nesh
def rrethnesh(request):
    cat_trainings = Category_training.objects.all()
    context = {"cat_trainings": cat_trainings}
    return render(request, "kryefaqja/rrethnesh.html", context)


# Politikat e privatesise
def policy(request):
    cat_trainings = Category_training.objects.all()
    # Subscribe
    if request.method == "POST":
        if request.POST.get("subscribe_email"):
            email = request.POST.get("subscribe_email")
            subscribe = Subscribe()
            subscribe.subscribe_email = request.POST.get("subscribe_email")
            if Subscribe.objects.filter(subscribe_email=email).exists():
                messages.warning(
                    request,
                    "Ju jeni bërë subscribe më parë në faqen tonë. Faleminderit !",
                )
            else:
                subscribe.save()
                messages.success(request, "Ju tashmë jeni pjesë e jona!")
    context = {"cat_trainings": cat_trainings}
    return render(request, "kryefaqja/politikat_privatesi.html", context)


# Termat dhe Kushtet
def terms(request):
    cat_trainings = Category_training.objects.all()

    # Subscribe
    if request.method == "POST":
        if request.POST.get("subscribe_email"):
            email = request.POST.get("subscribe_email")
            subscribe = Subscribe()
            subscribe.subscribe_email = request.POST.get("subscribe_email")
            if Subscribe.objects.filter(subscribe_email=email).exists():
                messages.warning(
                    request,
                    "Ju jeni bërë subscribe më parë në faqen tonë. Faleminderit !",
                )
            else:
                subscribe.save()
                messages.success(request, "Ju tashmë jeni pjesë e jona!")
    context = {"cat_trainings": cat_trainings}
    return render(request, "kryefaqja/termat_kushtet.html", context)
# function for 404 page
def error_404(request, exception):
    cat_trainings = Category_training.objects.all()
    context = {"cat_trainings": cat_trainings}
    return render(request, "404_page.html", context, status=404)
