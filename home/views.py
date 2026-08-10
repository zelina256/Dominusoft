from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import *
from trainings.models import *

# from contact.models import *
from apply.models import *
from datetime import date


# Search
def searchvenues(request):
    cat_trainings = Category_training.objects.all()
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
    if request.method == "POST":
        searched = request.POST.get("search")
        if searched:
            venues = Training.objects.filter(training_name__contains=searched)
            if venues:
                context = {
                    "searched": searched,
                    "venues": venues,
                    "cat_trainings": cat_trainings,
                }
                return render(request, "search/search.html", context)
            else:
                messages.info(request, " ")
        else:
            return HttpResponseRedirect("/search/")
    context = {"cat_trainings": cat_trainings}
    return render(request, "search/search.html", context)


# Kryefaqja
def home(request):
    partners = Partner.objects.all()
    cat_trainings = Category_training.objects.all()
    training = Training.objects.all()

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
        "training": training,
    }
    return render(request, "kryefaqja/kryefaqja.html", context)


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


def about(request):
    return render(request, "kryefaqja/rrethnesh.html")