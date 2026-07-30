from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import *
from trainings.models import *
from apply.models import *

# Create your views here.

# Projekt-Kursantesh
def project(request):
    cat_trainings = Category_training.objects.all()
    category_students = Student_Project_Category.objects.all()
    students_projects = Student_work.objects.all().order_by("student_project_id")[::-1]

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
        "students_projects": students_projects,
        "category_students": category_students,
    }
    return render(request, "projekte_studentesh/projekte_studentesh.html", context)
