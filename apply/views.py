from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from services.models import Services
from trainings.models import *
from apply.models import *


# Create your views here.


def _add_errors(request, errors, tag):
    for error in errors:
        messages.add_message(request, messages.ERROR, error, extra_tags=tag)


def _validate_email_address(email, label):
    if not email:
        return f"{label} është i detyrueshëm."
    try:
        validate_email(email)
    except ValidationError:
        return f"{label} nuk është i vlefshëm."
    return None


def _validate_phone(phone):
    if not phone:
        return "Numri i telefonit është i detyrueshëm."
    clean_phone = str(phone).strip().replace(" ", "")
    if not clean_phone.replace("+", "", 1).isdigit():
        return "Numri i telefonit duhet të përmbajë vetëm shifra."
    if len(clean_phone) < 6 or len(clean_phone) > 20:
        return "Numri i telefonit duhet të jetë nga 6 deri në 20 karaktere."
    return None


# Form Biznes
def business(request):
    cat_trainings = Category_training.objects.all()
    services = Services.objects.all()
    if request.method == "POST" and "business_button" in request.POST:
        name_business = (request.POST.get("name") or "").strip()
        delegate_business = (request.POST.get("delegate") or "").strip()
        email_business = (request.POST.get("email") or "").strip()
        phone_business = (request.POST.get("phone") or "").strip()
        service_business = (request.POST.get("service") or "").strip()
        message_business = (request.POST.get("message") or "").strip()

        errors = []
        if not name_business:
            errors.append("Emri i kompanisë është i detyrueshëm.")
        if not delegate_business:
            errors.append("Përfaqësuesi është i detyrueshëm.")

        email_error = _validate_email_address(email_business, "Email")
        if email_error:
            errors.append(email_error)

        phone_error = _validate_phone(phone_business)
        if phone_error:
            errors.append(phone_error)

        selected_service = Services.objects.filter(services_name=service_business).first()
        if not selected_service:
            errors.append("Shërbimi i zgjedhur nuk është i vlefshëm.")

        if not message_business:
            errors.append("Mesazhi është i detyrueshëm.")

        if not errors:
            Business.objects.create(
                business_name=name_business,
                business_delegate=delegate_business,
                business_email=email_business,
                business_phone=phone_business,
                business_service=selected_service,
                business_message=message_business,
            )
            messages.add_message(
                request,
                messages.SUCCESS,
                "Aplikimi u dërgua me sukses.",
                extra_tags="business",
            )
            return redirect("business")
        _add_errors(request, errors, "business")

    # Subscribe
    if request.method == "POST" and "subscribe_button" in request.POST:
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
        "services": services,
    }
    return render(request, "apliko/biznes.html", context)


# Form Staf
def career(request):
    cat_trainings = Category_training.objects.all()
    if request.method == "POST" and "career_button" in request.POST:
        name_staff = (request.POST.get("name") or "").strip()
        surname_staff = (request.POST.get("surname") or "").strip()
        email_staff = (request.POST.get("email") or "").strip()
        phone_staff = (request.POST.get("phone") or "").strip()
        job_staff = (request.POST.get("job") or "").strip()
        cv_staff = request.FILES.get("cv")
        message_staff = (request.POST.get("message") or "").strip()

        errors = []
        if not name_staff:
            errors.append("Emri është i detyrueshëm.")
        if not surname_staff:
            errors.append("Mbiemri është i detyrueshëm.")

        email_error = _validate_email_address(email_staff, "Email")
        if email_error:
            errors.append(email_error)

        phone_error = _validate_phone(phone_staff)
        if phone_error:
            errors.append(phone_error)

        if not job_staff:
            errors.append("Pozicioni i punës është i detyrueshëm.")
        if not cv_staff:
            errors.append("CV është i detyrueshëm.")
        if not message_staff:
            errors.append("Mesazhi është i detyrueshëm.")

        if not errors:
            NewStaff.objects.create(
                staff_name=name_staff,
                staff_surname=surname_staff,
                staff_email=email_staff,
                staff_phone=phone_staff,
                staff_position=job_staff,
                staff_cv=cv_staff,
                staff_message=message_staff,
            )
            messages.add_message(
                request,
                messages.SUCCESS,
                "Aplikimi u dërgua me sukses.",
                extra_tags="staf",
            )
            return redirect("career")
        _add_errors(request, errors, "staf")

    # Subscribe
    if request.method == "POST" and "subscribe_button" in request.POST:
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
    }
    return render(request, "apliko/karriera.html", context)


# Form Kursant
def student(request):
    # Subscribe
    if request.method == "POST" and "subscribe_button" in request.POST:
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

    cat_trainings = Category_training.objects.all()
    trainings = Training.objects.all()
    if request.method == "POST" and "student_button" in request.POST:
        name_student = (request.POST.get("name") or "").strip()
        surname_student = (request.POST.get("surname") or "").strip()
        email_student = (request.POST.get("email") or "").strip()
        phone_student = (request.POST.get("phone") or "").strip()
        training_student = (request.POST.get("training") or "").strip()
        message_student = (request.POST.get("message") or "").strip()

        errors = []
        if not name_student:
            errors.append("Emri është i detyrueshëm.")
        if not surname_student:
            errors.append("Mbiemri është i detyrueshëm.")

        email_error = _validate_email_address(email_student, "Email")
        if email_error:
            errors.append(email_error)

        phone_error = _validate_phone(phone_student)
        if phone_error:
            errors.append(phone_error)

        selected_training = Training.objects.filter(training_name=training_student).first()
        if not selected_training:
            errors.append("Trajnimi i zgjedhur nuk është i vlefshëm.")

        if not message_student:
            errors.append("Mesazhi është i detyrueshëm.")

        if not errors:
            Student.objects.create(
                student_name=name_student,
                student_surname=surname_student,
                student_email=email_student,
                student_phone=phone_student,
                student_training=selected_training,
                student_message=message_student,
            )
            messages.add_message(
                request,
                messages.SUCCESS,
                "Aplikimi u dërgua me sukses.",
                extra_tags="student",
            )
            return redirect("student")
        _add_errors(request, errors, "student")
    context = {
        "cat_trainings": cat_trainings,
        "trainings": trainings,
    }
    return render(request, "apliko/student.html", context)




def contact(request):
    cat_trainings = Category_training.objects.all()
    context = {
        "cat_trainings": cat_trainings,
    }
    return render(request, "apliko/contact.html", context)