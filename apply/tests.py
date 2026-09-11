from django.test import TestCase
from django.urls import reverse

from services.models import Services
from trainings.models import Training

from .models import Business, Contact, Student

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
