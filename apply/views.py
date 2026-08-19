from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import *
from services.models import Services
from trainings.models import *
from apply.models import *
import requests


# Create your views here.


# Form Biznes
def business(request):
    cat_trainings = Category_training.objects.all()
    services = Services.objects.all()
    if request.method == "POST" and "business_button" in request.POST:
        new_business = Business()
        name_business = request.POST.get("name")
        delegate_business = request.POST.get("delegate")
        email_business = request.POST.get("email")
        phone_business = request.POST.get("phone")
        service_business = request.POST.get("service")
        message_business = request.POST.get("message")

        new_business = Business(
            business_name=name_business,
            business_delegate=delegate_business,
            business_email=email_business,
            business_phone=phone_business,
            business_service=Services.objects.get(services_name=service_business),
            business_message=message_business,
        )

        new_business.save()

        #  reCAPTCHA validation
        recaptcha_response = request.POST.get("g-recaptcha-response")
        data = {
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        }
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        result = r.json()

        """ if reCAPTCHA returns True """
        if result["success"]:
            ctx = {
                "nameBusiness": name_business,
                "delegateBusiness": delegate_business,
                "emailBusiness": email_business,
                "phoneBusiness": phone_business,
                "serviceBusiness": service_business,
                "messageBusiness": message_business,
            }
            """ Send email """
            message = render_to_string("apliko/email/email_business.html", ctx)
            subject = "Biznesi-Shërbim"

            try:
                msg = EmailMultiAlternatives(
                    subject, message, "info@dominusoft.al", ["info@dominusoft.al"]
                )
                msg.attach_alternative(message, "text/html")
                msg.send()
            except BadHeaderError:
                return HttpResponse("Nuk gjendet.")
            messages.add_message(
                request, messages.SUCCESS, "Mesazhi u dërgua.", extra_tags="business"
            )
            return redirect("business")
        else:
            """if reCAPTCHA returns False"""
            messages.add_message(
                request,
                messages.ERROR,
                "Invalid reCAPTCHA. Provo përsëri.",
                extra_tags="business",
            )

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
        "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY,
    }
    return render(request, "apliko/biznes.html", context)


# Form Staf
def career(request):
    cat_trainings = Category_training.objects.all()
    if request.method == "POST" and "career_button" in request.POST:
        new_staff = NewStaff()
        name_staff = request.POST.get("name")
        surname_staff = request.POST.get("surname")
        email_staff = request.POST.get("email")
        phone_staff = request.POST.get("phone")
        job_staff = request.POST.get("job")
        cv_staff = request.FILES.get("cv")
        message_staff = request.POST.get("message")

        new_staff = NewStaff(
            staff_name=name_staff,
            staff_surname=surname_staff,
            staff_email=email_staff,
            staff_phone=phone_staff,
            staff_position=job_staff,
            staff_cv=cv_staff,
            staff_message=message_staff,
        )

        new_staff.save()

        # reCAPTCHA validation
        recaptcha_response = request.POST.get("g-recaptcha-response")
        data = {
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        }
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        result = r.json()

        """ if reCAPTCHA returns True """
        if result["success"]:
            ctx = {
                "nameStaff": name_staff,
                "surnameStaff": surname_staff,
                "emailStaff": email_staff,
                "phoneStaff": phone_staff,
                "jobStaff": job_staff,
                "cvStaff": cv_staff,
                "messageStaff": message_staff,
            }

            """ Send email """
            message = render_to_string("apliko/email/email_staf.html", ctx)
            subject = "Karriera-Staf"

            try:
                msg = EmailMultiAlternatives(
                    subject, message, "info@dominusoft.al", ["info@dominusoft.al"]
                )
                msg.attach_alternative(message, "text/html")
                msg.send()
            except BadHeaderError:
                return HttpResponse("Nuk gjendet.")
            messages.add_message(
                request, messages.SUCCESS, "Mesazhi u dërgua.", extra_tags="staf"
            )
            return redirect("career")
        else:
            """if reCAPTCHA returns False"""
            messages.add_message(
                request,
                messages.ERROR,
                "Invalid reCAPTCHA. Provo përsëri.",
                extra_tags="staf",
            )

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
        "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY,
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
        name_student = request.POST.get("name")
        surname_student = request.POST.get("surname")
        email_student = request.POST.get("email")
        phone_student = request.POST.get("phone")
        training_student = request.POST.get("training")
        message_student = request.POST.get("message")

        new_student = Student(
            student_name=name_student,
            student_surname=surname_student,
            student_email=email_student,
            student_phone=phone_student,
            student_training=Training.objects.get(training_name=training_student),
            student_message=message_student,
        )

        new_student.save()
        #  reCAPTCHA validation
        recaptcha_response = request.POST.get("g-recaptcha-response")
        data = {
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        }
        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
        result = r.json()

        """ if reCAPTCHA returns True """
        if result["success"]:
            ctx = {
                "nameStudent": name_student,
                "surnameStudent": surname_student,
                "emailStudent": email_student,
                "phoneStudent": phone_student,
                "trainingStudent": training_student,
                "messageStudent": message_student,
            }

            """ Send email """
            message = render_to_string("apliko/email/email_kursant.html", ctx)
            subject = "Kursant i interesuar"

            try:
                msg = EmailMultiAlternatives(
                    subject, message, "info@dominusoft.al", ["info@dominusoft.al"]
                )
                msg.attach_alternative(message, "text/html")
                msg.send()
            except BadHeaderError:
                return HttpResponse("Nuk gjendet.")
            messages.add_message(
                request, messages.SUCCESS, "Mesazhi u dërgua.", extra_tags="student"
            )
            return redirect("student")
        else:
            """if reCAPTCHA returns False"""
            messages.add_message(
                request,
                messages.ERROR,
                "Invalid reCAPTCHA. Provo përsëri.",
                extra_tags="student",
            )
    context = {
        "cat_trainings": cat_trainings,
        "trainings": trainings,
        "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY,
    }
    return render(request, "apliko/student.html", context)


# Kontakt
def contact(request):
    cat_trainings = Category_training.objects.all()
    context = {"cat_trainings": cat_trainings}
    return render(request, "apliko/contact.html", context)
