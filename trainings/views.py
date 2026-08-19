from django.shortcuts import get_object_or_404, render

from .models import Career, Category_training, Curricula, Lesson, Project, Training

# Create your views here.


def training_category(request):
    cat_trainings = Category_training.objects.all().order_by("cat_training_id")
    trainings = Training.objects.select_related("training_category").all()
    context = {"cat_trainings": cat_trainings, "trainings": trainings}
    return render(request, "trajnime/kategori.html", context)


def trainings(request, slug_training):
    cat_trainings = Category_training.objects.all().order_by("cat_training_id")
    trainings = Training.objects.select_related("training_category").all()
    cat_training = get_object_or_404(Category_training, cat_slug=slug_training)
    training = Training.objects.filter(training_category=cat_training).order_by(
        "training_id"
    )
    context = {
        "cat_trainings": cat_trainings,
        "cat_training": cat_training,
        "trainings": trainings,
        "training": training,
    }
    return render(request, "trajnime/trajnime_kat.html", context)


def curricula(request, slug_training, kurrikula_slug):
    cat_trainings = Category_training.objects.all().order_by("cat_training_id")
    trainings = Training.objects.select_related("training_category").all()
    cat_training = get_object_or_404(Category_training, cat_slug=slug_training)
    training = get_object_or_404(
        Training,
        training_slug=kurrikula_slug,
        training_category=cat_training,
    )
    careers = Career.objects.filter(career_training=training)
    projects = Project.objects.filter(project_training=training)
    curriculas = Curricula.objects.filter(curricula_train=training)
    lessons = Lesson.objects.filter(lesson_curricula=curriculas)
    same_training = Training.objects.filter(
        training_category=cat_training
    ).exclude(pk=training.pk).order_by("training_id")[:3]
    context = {
        "cat_trainings": cat_trainings,
        "training": training,
        "trainings": trainings,
        "careers": careers,
        "projects": projects,
        "curriculas": curriculas,
        "lessons": lessons,
        "cat_training": cat_training,
        "same_training": same_training,
    }
    return render(request, "trajnime/kurrikula.html", context)
