from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime
import json
import logging
import re
from urllib import error, request as urllib_request
from services.models import Services
from trainings.models import *
from apply.models import *


logger = logging.getLogger(__name__)


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


def _validate_required_text(value, label, min_length=1, max_length=None):
    clean_value = (value or "").strip()
    if not clean_value:
        return f"{label} është i detyrueshëm."
    if len(clean_value) < min_length:
        return f"{label} duhet të ketë të paktën {min_length} karaktere."
    if max_length is not None and len(clean_value) > max_length:
        return f"{label} duhet të ketë maksimumi {max_length} karaktere."
    return None


def _validate_birthday(birthday_value):
    if not birthday_value:
        return "Ditëlindja është e detyrueshme."

    try:
        birthday = datetime.datetime.strptime(birthday_value, "%Y-%m-%d").date()
    except ValueError:
        return "Ditëlindja nuk është në format të vlefshëm."

    today = timezone.now().date()
    if birthday > today:
        return "Ditëlindja nuk mund të jetë në të ardhmen."
    if birthday.year < 1900:
        return "Ditëlindja nuk është e vlefshme."
    return None


def _validate_card_id_number(card_id_number):
    if not card_id_number:
        return "Numri i kartës së identitetit është i detyrueshëm."
    clean_value = card_id_number.strip().upper()
    if not re.match(r"^[A-Z0-9]{5,20}$", clean_value):
        return "Numri i kartës së identitetit nuk është i vlefshëm."
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


def _validate_card_number(card_number_value):
    card_digits = re.sub(r"\D", "", card_number_value or "")
    if not card_digits:
        return "Numri i kartës është i detyrueshëm."
    if len(card_digits) < 13 or len(card_digits) > 19:
        return "Numri i kartës duhet të ketë nga 13 deri në 19 shifra."
    if not _luhn_check(card_digits):
        return "Numri i kartës nuk është i vlefshëm."
    return None


def _validate_card_expiry(expiry_value):
    if not expiry_value:
        return "Skadenca e kartës është e detyrueshme."

    match = re.match(r"^(0[1-9]|1[0-2])/(\d{2})$", expiry_value.strip())
    if not match:
        return "Skadenca duhet të jetë në formatin MM/YY."

    month = int(match.group(1))
    year = 2000 + int(match.group(2))
    today = timezone.now().date()

    if year < today.year:
        return "Karta ka skaduar."
    if year == today.year and month < today.month:
        return "Karta ka skaduar."
    return None


def _validate_card_cvv(cvv_value):
    cvv_digits = re.sub(r"\D", "", cvv_value or "")
    if not cvv_digits:
        return "CVV është i detyrueshëm."
    if len(cvv_digits) not in (3, 4):
        return "CVV duhet të ketë 3 ose 4 shifra."
    return None


def _authorize_card_payment(
    cardholder_name,
    card_number,
    card_expiry,
    card_cvv,
    student_email,
    training,
):
    gateway_url = str(getattr(settings, "BANK_PAYMENT_API_URL", "")).strip()
    if not gateway_url:
        return False, "Pagesa nuk mund të kryhet aktualisht. Ju lutem kontaktoni stafin tonë."

    card_digits = re.sub(r"\D", "", card_number or "")
    payload = {
        "cardholder_name": cardholder_name,
        "card_number": card_digits,
        "card_expiry": card_expiry,
        "card_cvv": card_cvv,
        "currency": "ALL",
        "reference": f"student-{timezone.now().strftime('%Y%m%d%H%M%S')}",
        "customer_email": student_email,
        "training_id": getattr(training, "pk", None),
        "training_name": getattr(training, "training_name", ""),
    }

    headers = {"Content-Type": "application/json"}
    api_key = str(getattr(settings, "BANK_PAYMENT_API_KEY", "")).strip()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    request_body = json.dumps(payload).encode("utf-8")
    bank_request = urllib_request.Request(
        gateway_url,
        data=request_body,
        headers=headers,
        method="POST",
    )

    try:
        with urllib_request.urlopen(bank_request, timeout=15) as response:
            raw_response = response.read().decode("utf-8")
            response_data = json.loads(raw_response) if raw_response else {}
    except error.HTTPError as http_error:
        try:
            error_data = json.loads(http_error.read().decode("utf-8"))
            message = error_data.get("message")
        except (json.JSONDecodeError, UnicodeDecodeError):
            message = None
        return False, message or "Pagesa u refuzua nga banka."
    except (error.URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError):
        return False, "Nuk u arrit lidhja me bankën. Provoni përsëri pas pak."

    approved = bool(response_data.get("approved"))
    status = str(response_data.get("status", "")).lower()
    if approved or status in {"approved", "success", "succeeded"}:
        return True, None

    return False, response_data.get("message") or "Pagesa nuk u aprovua nga banka."


def _send_student_procedure_email(student_data):
    student_email = student_data.get("email")
    if not student_email:
        return False

    subject = "Konfirmim aplikimi dhe pagese - Dominusoft"
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@dominusoft.com")

    html_body = render_to_string("apliko/email/email_kursant.html", student_data)
    text_body = strip_tags(html_body)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=[student_email],
    )
    email.attach_alternative(html_body, "text/html")

    try:
        email.send(fail_silently=False)
        return True
    except Exception:
        logger.exception("Failed to send student procedure email")
        return False


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
            return render(
                request,
                "apliko/biznes.html",
                {
                    "cat_trainings": cat_trainings,
                    "services": services,
                    "show_business_success_modal": True,
                },
            )
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
        "show_business_success_modal": False,
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
        father_name_student = (request.POST.get("father_name") or "").strip()
        birthday_student = (request.POST.get("birthday") or "").strip()
        email_student = (request.POST.get("email") or "").strip()
        phone_student = (request.POST.get("phone") or "").strip()
        card_id_number_student = (request.POST.get("card_id_number") or "").strip()
        university_degree_student = (request.POST.get("university_degree") or "").strip()
        training_student = (request.POST.get("training") or "").strip()
        timetable_student = (request.POST.get("timetable") or "").strip()
        message_student = (request.POST.get("message") or "").strip()
        terms_conditions_student = (request.POST.get("terms_conditions") or "").strip()
        cardholder_name_student = (request.POST.get("cardholder_name") or "").strip()
        card_number_student = (request.POST.get("card_number") or "").strip()
        card_expiry_student = (request.POST.get("card_expiry") or "").strip()
        card_cvv_student = (request.POST.get("card_cvv") or "").strip()

        errors = []

        name_error = _validate_required_text(name_student, "Emri", max_length=50)
        if name_error:
            errors.append(name_error)

        surname_error = _validate_required_text(surname_student, "Mbiemri", max_length=50)
        if surname_error:
            errors.append(surname_error)

        father_name_error = _validate_required_text(
            father_name_student, "Emri i babait", max_length=100
        )
        if father_name_error:
            errors.append(father_name_error)

        birthday_error = _validate_birthday(birthday_student)
        if birthday_error:
            errors.append(birthday_error)

        email_error = _validate_email_address(email_student, "Email")
        if email_error:
            errors.append(email_error)

        phone_error = _validate_phone(phone_student)
        if phone_error:
            errors.append(phone_error)

        card_id_error = _validate_card_id_number(card_id_number_student)
        if card_id_error:
            errors.append(card_id_error)

        degree_error = _validate_allowed_choice(
            university_degree_student,
            {"bachelor", "master", "doctorate", "other"},
            "Diploma universitare",
        )
        if degree_error:
            errors.append(degree_error)

        timetable_error = _validate_allowed_choice(
            timetable_student,
            {"morning", "afternoon", "evening"},
            "Orari i preferuar",
        )
        if timetable_error:
            errors.append(timetable_error)

        selected_training = Training.objects.filter(pk=training_student).first()
        if not selected_training and training_student:
            selected_training = Training.objects.filter(training_name=training_student).first()
        if not selected_training:
            errors.append("Trajnimi i zgjedhur nuk është i vlefshëm.")

        message_error = _validate_required_text(message_student, "Mesazhi", max_length=300)
        if message_error:
            errors.append(message_error)

        if terms_conditions_student != "accepted":
            errors.append("Duhet të pranoni termat dhe kushtet.")

        cardholder_error = _validate_required_text(
            cardholder_name_student,
            "Emri në kartë",
            min_length=3,
            max_length=100,
        )
        if cardholder_error:
            errors.append(cardholder_error)

        card_number_error = _validate_card_number(card_number_student)
        if card_number_error:
            errors.append(card_number_error)

        card_expiry_error = _validate_card_expiry(card_expiry_student)
        if card_expiry_error:
            errors.append(card_expiry_error)

        card_cvv_error = _validate_card_cvv(card_cvv_student)
        if card_cvv_error:
            errors.append(card_cvv_error)

        if not errors:
            payment_ok, payment_error = _authorize_card_payment(
                cardholder_name_student,
                card_number_student,
                card_expiry_student,
                card_cvv_student,
                email_student,
                selected_training,
            )

            if not payment_ok:
                _add_errors(request, [payment_error], "student")
                context = {
                    "cat_trainings": cat_trainings,
                    "trainings": trainings,
                }
                return render(request, "apliko/student.html", context)

            birthday_date = datetime.datetime.strptime(birthday_student, "%Y-%m-%d").date()
            student_application = Student.objects.create(
                student_name=name_student,
                student_surname=surname_student,
                student_father_name=father_name_student,
                student_birthday=birthday_date,
                student_email=email_student,
                student_phone=phone_student,
                student_card_id_number=card_id_number_student.upper(),
                student_university_degree=university_degree_student,
                student_training=selected_training,
                student_timetable=timetable_student,
                student_terms_accepted=True,
                student_message=message_student,
            )

            email_sent = _send_student_procedure_email(
                {
                    "nameStudent": name_student,
                    "surnameStudent": surname_student,
                    "emailStudent": email_student,
                    "phoneStudent": phone_student,
                    "trainingStudent": getattr(selected_training, "training_name", ""),
                    "timetableStudent": timetable_student,
                    "messageStudent": message_student,
                    "applicationDate": timezone.localtime(student_application.submit_at),
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
            return render(
                request,
                "apliko/student.html",
                {
                    "cat_trainings": cat_trainings,
                    "trainings": trainings,
                    "show_student_success_modal": True,
                },
            )
        _add_errors(request, errors, "student")
    context = {
        "cat_trainings": cat_trainings,
        "trainings": trainings,
        "show_student_success_modal": False,
    }
    return render(request, "apliko/student.html", context)




def contact(request):
    cat_trainings = Category_training.objects.all()
    form_data = {
        "name": "",
        "surname": "",
        "email": "",
        "phone": "",
        "subject": "",
        "message": "",
    }
    field_errors = {}

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

    if request.method == "POST" and "subscribe_button" not in request.POST:
        form_data["name"] = (request.POST.get("name") or "").strip()
        form_data["surname"] = (request.POST.get("surname") or "").strip()
        form_data["email"] = (request.POST.get("email") or "").strip()
        form_data["phone"] = (request.POST.get("phone") or "").strip()
        form_data["subject"] = (request.POST.get("subject") or "").strip()
        form_data["message"] = (request.POST.get("message") or "").strip()

        errors = []

        name_error = _validate_required_text(form_data["name"], "Emri", max_length=50)
        if name_error:
            field_errors["name"] = name_error
            errors.append(name_error)

        surname_error = _validate_required_text(form_data["surname"], "Mbiemri", max_length=50)
        if surname_error:
            field_errors["surname"] = surname_error
            errors.append(surname_error)

        email_error = _validate_email_address(form_data["email"], "Email")
        if email_error:
            field_errors["email"] = email_error
            errors.append(email_error)

        phone_error = _validate_phone(form_data["phone"])
        if phone_error:
            field_errors["phone"] = phone_error
            errors.append(phone_error)

        subject_error = _validate_required_text(
            form_data["subject"],
            "Subjekti",
            min_length=3,
            max_length=200,
        )
        if subject_error:
            field_errors["subject"] = subject_error
            errors.append(subject_error)

        message_error = _validate_required_text(
            form_data["message"],
            "Mesazhi",
            min_length=10,
            max_length=1000,
        )
        if message_error:
            field_errors["message"] = message_error
            errors.append(message_error)

        if not errors:
            Contact.objects.create(
                contact_name=form_data["name"],
                contact_surname=form_data["surname"],
                contact_email=form_data["email"],
                contact_phone=form_data["phone"],
                contact_subject=form_data["subject"],
                contact_message=form_data["message"],
            )
            messages.add_message(
                request,
                messages.SUCCESS,
                "Mesazhi juaj u dërgua me sukses.",
                extra_tags="contact",
            )
            context = {
                "cat_trainings": cat_trainings,
                "form_data": {
                    "name": "",
                    "surname": "",
                    "email": "",
                    "phone": "",
                    "subject": "",
                    "message": "",
                },
                "field_errors": {},
                "show_contact_success_modal": True,
            }
            return render(request, "apliko/contact.html", context)

        _add_errors(request, errors, "contact")

    context = {
        "cat_trainings": cat_trainings,
        "form_data": form_data,
        "field_errors": field_errors,
        "show_contact_success_modal": False,
    }
    return render(request, "apliko/contact.html", context)