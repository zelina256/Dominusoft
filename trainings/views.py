from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import *
from trainings.models import *

# from contact.models import *
from apply.models import *

# Create your views here.


def training_category(request):
    cat_trainings = Category_training.objects.all()
    trainings = Training.objects.all()

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
    context = {"cat_trainings": cat_trainings, "trainings": trainings}
    return render(request, "trajnime/kategori.html", context)


def trainings(request, slug_training):
    cat_trainings = Category_training.objects.all()
    trainings = Training.objects.all()
    # 404
    cat_training = get_object_or_404(Category_training, cat_slug=slug_training)
    training = Training.objects.filter(training_category=cat_training)

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
        "cat_trainings": cat_trainings,
        "cat_training": cat_training,
        "trainings": trainings,
        "training": training,
    }
    return render(request, "trajnime/trajnime_kat.html", context)


import random

def curricula(request, slug_training, kurrikula_slug):
    cat_trainings = Category_training.objects.all()
    trainings = Training.objects.all()
    # 404
    training = get_object_or_404(Training, training_slug=kurrikula_slug)
    careers = Career.objects.filter(career_training=training)
    projects = Project.objects.filter(project_training=training)
    curriculas = Curricula.objects.filter(curricula_train=training)
    lessons = Lesson.objects.filter(lesson_curricula=curriculas)
    cat_training = get_object_or_404(Category_training, cat_slug=slug_training)
    same_training = Training.objects.filter(training_category=cat_training)
    items = list(same_training)
    sample_size = min(len(items), 3)
    if len(items) > 0:
        random_items = random.sample(items, sample_size)
    else:
        random_items = []
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
        "cat_trainings": cat_trainings,
        "training": training,
        "trainings": trainings,
        "careers": careers,
        "projects": projects,
        "curriculas": curriculas,
        "lessons": lessons,
        "cat_training": cat_training,
        "same_training": random_items,
    }
    return render(request, "trajnime/kurrikula.html", context)
