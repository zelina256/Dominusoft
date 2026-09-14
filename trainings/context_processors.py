from .models import Category_training


def training_categories(request):
    return {
        "cat_trainings": Category_training.objects.all().order_by("cat_training_id")
    }