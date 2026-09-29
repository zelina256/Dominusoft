from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime
import json
import logging
import re
import uuid
from urllib import error, parse, request as urllib_request
from services.models import Services
from trainings.models import *
from apply.models import *


logger = logging.getLogger(__name__)


def _add_errors(request, errors, tag):
    for error in errors:
        messages.add_message(request, messages.ERROR, error, extra_tags=tag)


def _is_honeypot_submission(request):
    return bool((request.POST.get("website") or "").strip())


def _get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _is_rate_limited(request, form_name):
    if not getattr(settings, "FORM_SUBMISSION_LIMIT", 0):
        return False

    cache_key = "application-form:%s:%s" % (form_name, _get_client_ip(request))
    current_count = cache.get(cache_key, 0)
    if current_count >= settings.FORM_SUBMISSION_LIMIT:
        return True

    cache.set(
        cache_key,
        current_count + 1,
        timeout=getattr(settings, "FORM_SUBMISSION_WINDOW_SECONDS", 3600),
    )
    return False


def _verify_recaptcha(request, action):
    if not getattr(settings, "RECAPTCHA_ENABLED", False):
        return True

    token = request.POST.get("g-recaptcha-response", "")
    if not token:
        return False

    payload = parse.urlencode(
        {
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": token,
            "remoteip": _get_client_ip(request),
        }
    ).encode("utf-8")
    verification_request = urllib_request.Request(
        "https://www.google.com/recaptcha/api/siteverify",
        data=payload,
    )

    try:
        with urllib_request.urlopen(verification_request, timeout=5) as response:
            verification_result = json.loads(response.read().decode("utf-8"))
    except (error.URLError, ValueError, OSError):
        logger.warning("reCAPTCHA verification failed", exc_info=True)
        return False

    return (
        verification_result.get("success") is True
        and verification_result.get("action") == action
        and verification_result.get("score", 0) >= 0.5
    )


def _has_spam_protection_failure(request, form_name, recaptcha_action):
    if not _verify_recaptcha(request, recaptcha_action):
        return True
    return _is_rate_limited(request, form_name)


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


def _validate_required_text(value, label, min_length=1, max_length=None):
    clean_value = (value or "").strip()
    if not clean_value:
        return f"{label} është i detyrueshëm."
    if len(clean_value) < min_length:
        return f"{label} duhet të ketë të paktën {min_length} karaktere."
    if max_length is not None and len(clean_value) > max_length:
        return f"{label} duhet të ketë maksimumi {max_length} karaktere."
    return None






def _validate_allowed_choice(value, allowed_values, label):
    if not value:
        return f"{label} është i detyrueshëm."
    if value not in allowed_values:
        return f"{label} nuk është i vlefshëm."
    return None


def _luhn_check(number_digits):
    checksum = 0
    parity = len(number_digits) % 2
    for index, digit_char in enumerate(number_digits):
        digit = int(digit_char)
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0





def _send_student_procedure_email(student_data):
    recipient = getattr(
        settings,
        "STUDENT_NOTIFICATION_EMAIL",
        getattr(settings, "DEFAULT_FROM_EMAIL", "info@dominusoft.al"),
    )
    if not recipient:
        return False

    subject = "Aplikim i ri për trajnim - Dominusoft"
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@dominusoft.com")

    email_context = {
        **student_data,
        "email_css_url": f"https://{settings.DOMAIN}{settings.STATIC_URL.rstrip('/')}/css/email.css",
    }
    html_body = render_to_string("apliko/email/email_kursant.html", email_context)
    text_body = strip_tags(html_body)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=[recipient],
    )
    email.attach_alternative(html_body, "text/html")

    try:
        email.send(fail_silently=False)
        return True
    except Exception:
        logger.exception("Failed to send student procedure email")
        return False


def _send_business_notification_email(business_data):
    recipient = getattr(
        settings,
        "BUSINESS_NOTIFICATION_EMAIL",
        getattr(settings, "DEFAULT_FROM_EMAIL", "info@dominusoft.al"),
    )
    if not recipient:
        return False

    email_context = {
        **business_data,
        "email_css_url": f"https://{settings.DOMAIN}{settings.STATIC_URL.rstrip('/')}/css/email.css",
    }
    html_body = render_to_string("apliko/email/email_business.html", email_context)
    email = EmailMultiAlternatives(
        subject="Aplikim i ri nga biznesi - Dominusoft",
        body=strip_tags(html_body),
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@dominusoft.com"),
        to=[recipient],
    )
    email.attach_alternative(html_body, "text/html")

    try:
        email.send(fail_silently=False)
        return True
    except Exception:
        logger.exception("Failed to send business notification email")
        return False



# Form Biznes
def business(request, template_name="apliko/biznes.html"):
    cat_trainings = Category_training.objects.all()
    services = Services.objects.all()
    form_data = {
        "submission_token": uuid.uuid4().hex,
        "name": "",
        "delegate": "",
        "email": "",
        "phone": "",
        "service": "",
        "message": "",
    }
    field_errors = {}

    if request.method == "POST" and "business_button" in request.POST:
        if _is_honeypot_submission(request):
            return redirect("application")
        if _has_spam_protection_failure(request, "business", "business_inquiry"):
            messages.add_message(
                request,
                messages.ERROR,
                "Kërkesa nuk mund të verifikohet. Ju lutem provoni përsëri.",
                extra_tags="business",
            )
            return redirect("application" if template_name == "apliko/application.html" else "business")

        form_data["submission_token"] = request.POST.get("submission_token") or ""
        form_data["name"] = (request.POST.get("name") or "").strip()
        form_data["delegate"] = (request.POST.get("delegate") or "").strip()
        form_data["email"] = (request.POST.get("email") or "").strip()
        form_data["phone"] = (request.POST.get("phone") or "").strip()
        form_data["service"] = (request.POST.get("service") or "").strip()
        form_data["message"] = (request.POST.get("message") or "").strip()

        errors = []
        if not re.fullmatch(r"[0-9a-f]{32}", form_data["submission_token"]):
            errors.append("Kërkesa nuk është e vlefshme. Ju lutem provoni përsëri.")

        name_error = _validate_required_text(form_data["name"], "Emri i kompanisë", max_length=100)
        if name_error:
            field_errors["name"] = name_error
            errors.append(name_error)

        delegate_error = _validate_required_text(form_data["delegate"], "Përfaqësuesi", max_length=100)
        if delegate_error:
            field_errors["delegate"] = delegate_error
            errors.append(delegate_error)

        email_error = _validate_email_address(form_data["email"], "Email")
        if email_error:
            field_errors["email"] = email_error
            errors.append(email_error)

        phone_error = _validate_phone(form_data["phone"])
        if phone_error:
            field_errors["phone"] = phone_error
            errors.append(phone_error)

        selected_service = Services.objects.filter(services_name=form_data["service"]).first()
        if not selected_service:
            service_error = "Shërbimi i zgjedhur nuk është i vlefshëm."
            field_errors["service"] = service_error
            errors.append(service_error)

        message_error = _validate_required_text(
            form_data["message"],
            "Mesazhi",
            min_length=10,
            max_length=300,
        )
        if message_error:
            field_errors["message"] = message_error
            errors.append(message_error)

        if not errors:
            _, created = Business.objects.get_or_create(
                submission_token=form_data["submission_token"],
                defaults={
                    "business_name": form_data["name"],
                    "business_delegate": form_data["delegate"],
                    "business_email": form_data["email"],
                    "business_phone": form_data["phone"],
                    "business_service": selected_service,
                    "business_message": form_data["message"],
                },
            )
            if created:
                _send_business_notification_email(
                    {
                        "nameBusiness": form_data["name"],
                        "delegateBusiness": form_data["delegate"],
                        "emailBusiness": form_data["email"],
                        "phoneBusiness": form_data["phone"],
                        "serviceBusiness": selected_service,
                        "messageBusiness": form_data["message"],
                    }
                )
            messages.add_message(
                request,
                messages.SUCCESS,
                "Aplikimi u dërgua me sukses.",
                extra_tags="business",
            )
            request.session["show_business_success_modal"] = True
            return redirect("application" if template_name == "apliko/application.html" else "business")
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
        "form_data": form_data,
        "field_errors": field_errors,
        "show_business_success_modal": request.session.pop("show_business_success_modal", False),
        "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY,
    }
    if template_name == "apliko/application.html":
        context.update(
            {
                "active_application_form": "business",
                "business_form_data": form_data,
                "business_field_errors": field_errors,
                "student_form_data": _student_form_data(),
                "student_field_errors": {},
                "trainings": Training.objects.all(),
                "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY,
            }
        )
    return render(request, template_name, context)

# Form Kursant
def _student_form_data():
    return {
        "submission_token": uuid.uuid4().hex,
        "name": "",
        "father_name": "",
        "surname": "",
        "birthday": "",
        "email": "",
        "phone": "",
        "card_id_number": "",
        "university_degree": "",
        "training": "",
        "timetable": "",
        "message": "",
        "terms_conditions": "",
    }


def student(request, template_name="apliko/student.html"):
    form_data = _student_form_data()
    field_errors = {}

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
        if _is_honeypot_submission(request):
            return redirect("application")
        if _has_spam_protection_failure(request, "student", "student_application"):
            messages.add_message(
                request,
                messages.ERROR,
                "Kërkesa nuk mund të verifikohet. Ju lutem provoni përsëri.",
                extra_tags="student",
            )
            return redirect("application" if template_name == "apliko/application.html" else "student")

        form_data["submission_token"] = request.POST.get("submission_token") or ""
        name_student = (request.POST.get("name") or "").strip()
        surname_student = (request.POST.get("surname") or "").strip()
        email_student = (request.POST.get("email") or "").strip()
        phone_student = (request.POST.get("phone") or "").strip()
        training_student = (request.POST.get("training") or "").strip()
        message_student = (request.POST.get("message") or "").strip()
        terms_conditions_student = (request.POST.get("terms_conditions") or "").strip()

        form_data.update(
            {
                "name": name_student,
                "surname": surname_student,
                "email": email_student,
                "phone": phone_student,
                "training": training_student,
                "message": message_student,
                "terms_conditions": terms_conditions_student,
            }
        )

        errors = []
        if not re.fullmatch(r"[0-9a-f]{32}", form_data["submission_token"]):
            errors.append("Kërkesa nuk është e vlefshme. Ju lutem provoni përsëri.")

        name_error = _validate_required_text(name_student, "Emri", max_length=50)
        if name_error:
            errors.append(name_error)
            field_errors["name"] = name_error

        surname_error = _validate_required_text(surname_student, "Mbiemri", max_length=50)
        if surname_error:
            errors.append(surname_error)
            field_errors["surname"] = surname_error


        email_error = _validate_email_address(email_student, "Email")
        if email_error:
            errors.append(email_error)
            field_errors["email"] = email_error

        phone_error = _validate_phone(phone_student)
        if phone_error:
            errors.append(phone_error)
            field_errors["phone"] = phone_error

        selected_training = None
        if training_student:
            selected_training = Training.objects.filter(pk=training_student).first()
            if not selected_training:
                selected_training = Training.objects.filter(training_name=training_student).first()
        if not selected_training:
            training_error = "Trajnimi i zgjedhur nuk është i vlefshëm."
            errors.append(training_error)
            field_errors["training"] = training_error

        message_error = None
        if len(message_student) > 300:
            message_error = "Mesazhi duhet të ketë maksimumi 300 karaktere."
        if message_error:
            errors.append(message_error)
            field_errors["message"] = message_error

        if terms_conditions_student != "accepted":
            terms_error = "Duhet të pranoni termat dhe kushtet."
            errors.append(terms_error)
            field_errors["terms_conditions"] = terms_error

        if not errors:
            student_application, created = Student.objects.get_or_create(
                submission_token=form_data["submission_token"],
                defaults={
                    "student_name": name_student,
                    "student_surname": surname_student,
                    "student_email": email_student,
                    "student_phone": phone_student,
                    "student_training": selected_training,
                    "student_terms_accepted": True,
                    "student_message": message_student,
                },
            )

            email_sent = True
            if created:
                email_sent = _send_student_procedure_email(
                    {
                        "nameStudent": name_student,
                        "surnameStudent": surname_student,
                        "emailStudent": email_student,
                        "phoneStudent": phone_student,
                        "trainingStudent": getattr(selected_training, "training_name", ""),
                        "messageStudent": message_student,
                        "applicationDate": student_application.submit_at,
                    }
                )

            messages.add_message(
                request,
                messages.SUCCESS,
                "Aplikimi u dërgua me sukses.",
                extra_tags="student",
            )
            if not email_sent:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Aplikimi u regjistrua, por email-i i konfirmimit nuk u dërgua.",
                    extra_tags="student",
                )
            request.session["show_student_success_modal"] = True
            return redirect("application" if template_name == "apliko/application.html" else "student")
    context = {
        "cat_trainings": cat_trainings,
        "trainings": trainings,
        "show_student_success_modal": request.session.pop("show_student_success_modal", False),
        "form_data": form_data,
        "field_errors": field_errors,
        "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY,
    }
    if template_name == "apliko/application.html":
        context.update(
            {
                "active_application_form": "student",
                "student_form_data": form_data,
                "student_field_errors": field_errors,
                "business_form_data": {
                    "submission_token": uuid.uuid4().hex,
                    "name": "",
                    "delegate": "",
                    "email": "",
                    "phone": "",
                    "service": "",
                    "message": "",
                },
                "business_field_errors": {},
                "services": Services.objects.all(),
            }
        )
    return render(request, template_name, context)


def application(request):
    if request.method == "POST" and "student_button" in request.POST:
        return student(request, "apliko/application.html")
    if request.method == "POST" and "business_button" in request.POST:
        return business(request, "apliko/application.html")

    requested_form = request.GET.get("form")
    active_application_form = requested_form if requested_form in {"student", "business"} else "student"
    requested_training = request.GET.get("training", "")
    selected_training_id = ""
    if requested_training and Training.objects.filter(pk=requested_training).exists():
        selected_training_id = requested_training

    requested_service = request.GET.get("service", "")
    selected_service_name = ""
    if requested_service:
        selected_service = Services.objects.filter(pk=requested_service).only(
            "services_name"
        ).first()
        if selected_service:
            selected_service_name = selected_service.services_name

    student_form_data = _student_form_data()
    student_form_data["training"] = selected_training_id
    business_form_data = {
        "submission_token": uuid.uuid4().hex,
        "name": "",
        "delegate": "",
        "email": "",
        "phone": "",
        "service": selected_service_name,
        "message": "",
    }

    return render(
        request,
        "apliko/application.html",
        {
            "cat_trainings": Category_training.objects.all(),
            "trainings": Training.objects.all(),
            "services": Services.objects.all(),
            "active_application_form": active_application_form,
            "show_student_success_modal": request.session.pop(
                "show_student_success_modal", False
            ),
            "show_business_success_modal": request.session.pop(
                "show_business_success_modal", False
            ),
            "student_form_data": student_form_data,
            "student_field_errors": {},
            "business_form_data": business_form_data,
            "business_field_errors": {},
            "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY,
        },
    )


def legacy_student(request):
    return redirect("application")


def legacy_business(request):
    return redirect("application")
