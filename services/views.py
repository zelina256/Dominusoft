from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import *
from trainings.models import *
from apply.models import *

# Sherbimet
def services(request):
    cat_trainings = Category_training.objects.all()
    services = Services.objects.all().order_by('-pk')
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
    context = {"cat_trainings": cat_trainings, "services": services}
    return render(request, "sherbime/sherbime.html", context)


def service_detail(request, services_slug):
    cat_trainings = Category_training.objects.all()
    service = get_object_or_404(Services, services_slug=services_slug)
    context = {"cat_trainings": cat_trainings, "service": service}
    return render(request, "sherbime/sherbimi_detail.html", context)