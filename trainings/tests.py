from django.test import TestCase
from django.urls import reverse

from .models import Category_training


class TrainingCategoryContextTests(TestCase):
	def test_training_categories_are_available_to_shared_navigation(self):
		category = Category_training.objects.create(
			cat_training_name="Programming",
			cat_slug="programming",
		)

		response = self.client.get(reverse("home"))

		self.assertContains(response, category.cat_training_name)
