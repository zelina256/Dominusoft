from django.shortcuts import render

from trainings.models import Category_training

from .models import Services

# Sherbimet
def services(request):
    cat_trainings = Category_training.objects.all().order_by("cat_training_id")
    services = Services.objects.all().order_by('-pk')
    context = {"cat_trainings": cat_trainings, "services": services}
    return render(request, "sherbime/sherbime.html", context)

def tech_services(request):
    return render(request, "sherbime/detaje_sherbime.html")