from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from services.models import Services
from trainings.models import Training

from .models import Business, Contact, Student

@override_settings(RECAPTCHA_ENABLED=False, FORM_SUBMISSION_LIMIT=0)
class ContactViewTests(TestCase):
	def test_repeated_submission_creates_one_contact(self):
		data = {
			"submission_token": "a" * 32,
			"name": "Arben",
			"surname": "Hoxha",
			"email": "arben@example.com",
			"phone": "+355 67 300 5050",
			"subject": "Kurs profesional",
			"message": "Dua informacion per kursin profesional.",
		}

		response = self.client.post(reverse("contact"), data)
		self.assertRedirects(response, reverse("contact"))

		response = self.client.post(reverse("contact"), data)
		self.assertRedirects(response, reverse("contact"))
		self.assertEqual(Contact.objects.count(), 1)

	def test_contact_submission_allows_an_empty_message(self):
		data = {
			"submission_token": "d" * 32,
			"name": "Arben",
			"surname": "Hoxha",
			"email": "arben@example.com",
			"phone": "+355 67 300 5050",
			"subject": "Kurs profesional",
			"message": "",
		}

		response = self.client.post(reverse("contact"), data)

		self.assertRedirects(response, reverse("contact"))
		contact = Contact.objects.get(submission_token=data["submission_token"])
		self.assertEqual(contact.contact_message, "")

	def test_repeated_submission_creates_one_business_request(self):
		service = Services.objects.create(services_name="Website")
		data = {
			"submission_token": "b" * 32,
			"name": "Dominusoft",
			"delegate": "Arben Hoxha",
			"email": "arben@example.com",
			"phone": "+355 67 300 5050",
			"service": service.services_name,
			"message": "Dua nje konsulte per projektin tone te ri.",
			"business_button": "",
		}

		response = self.client.post(reverse("business"), data)
		self.assertRedirects(response, reverse("business"))

		response = self.client.post(reverse("business"), data)
		self.assertRedirects(response, reverse("business"))
		self.assertEqual(Business.objects.count(), 1)

	def test_repeated_submission_creates_one_student_application(self):
		training = Training.objects.create(training_name="Web Development")
		data = {
			"submission_token": "c" * 32,
			"name": "Arben",
			"father_name": "Ilir",
			"surname": "Hoxha",
			"birthday": "2000-01-01",
			"email": "arben@example.com",
			"phone": "+355 67 300 5050",
			"card_id_number": "A12345678B",
			"university_degree": "bachelor",
			"training": str(training.pk),
			"timetable": "morning",
			"message": "Dua informacion per kursin profesional.",
			"terms_conditions": "accepted",
			"student_button": "",
		}

		response = self.client.post(reverse("student"), data)
		self.assertRedirects(response, reverse("student"))

		response = self.client.post(reverse("student"), data)
		self.assertRedirects(response, reverse("student"))
		self.assertEqual(Student.objects.count(), 1)

	def test_application_course_form_creates_student_application(self):
		training = Training.objects.create(training_name="Web Development")
		data = {
			"submission_token": "f" * 32,
			"name": "Arben",
			"surname": "Hoxha",
			"email": "arben@example.com",
			"phone": "+355 67 300 5050",
			"training": str(training.pk),
			"message": "Dua më shumë informacion për orarin e kursit.",
			"terms_conditions": "accepted",
			"student_button": "",
		}

		response = self.client.post(reverse("application"), data)

		self.assertRedirects(response, reverse("application"))
		student = Student.objects.get(submission_token=data["submission_token"])
		self.assertEqual(student.student_training, training)
		self.assertTrue(student.student_terms_accepted)
		self.assertEqual(student.student_message, data["message"])

	def test_application_preselects_training_from_query_parameter(self):
		training = Training.objects.create(training_name="Web Development")

		response = self.client.get(
			reverse("application"),
			{"form": "student", "training": training.pk},
		)

		self.assertContains(
			response,
			f'<option value="{training.pk}" selected>{training.training_name}</option>',
			html=True,
		)

	def test_application_preselects_service_from_query_parameter(self):
		service = Services.objects.create(services_name="Website")

		response = self.client.get(
			reverse("application"),
			{"form": "business", "service": service.pk},
		)

		self.assertContains(
			response,
			f'<option value="{service.services_name}" selected>{service.services_name}</option>',
			html=True,
		)

	def test_application_course_form_shows_training_validation_error(self):
		data = {
			"submission_token": "g" * 32,
			"name": "Arben",
			"surname": "Hoxha",
			"email": "arben@example.com",
			"phone": "+355 67 300 5050",
			"terms_conditions": "accepted",
			"student_button": "",
		}

		response = self.client.post(reverse("application"), data)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Trajnimi i zgjedhur nuk është i vlefshëm.")

	def test_student_submission_allows_empty_optional_fields(self):
		training = Training.objects.create(training_name="Web Development")
		data = {
			"submission_token": "e" * 32,
			"name": "Arben",
			"father_name": "Ilir",
			"surname": "Hoxha",
			"birthday": "",
			"email": "arben@example.com",
			"phone": "+355 67 300 5050",
			"card_id_number": "",
			"university_degree": "bachelor",
			"training": str(training.pk),
			"timetable": "morning",
			"message": "",
			"terms_conditions": "accepted",
			"student_button": "",
		}

		response = self.client.post(reverse("student"), data)

		self.assertRedirects(response, reverse("student"))
		student = Student.objects.get(submission_token=data["submission_token"])
		self.assertIsNone(student.student_birthday)
		self.assertIsNone(student.student_card_id_number)
		self.assertEqual(student.student_message, "")
