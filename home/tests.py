import json
import re
from datetime import timedelta
from tempfile import TemporaryDirectory

from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apply.models import Subscribe
from blog.models import Article
from home.models import Partner
from services.models import Services
from trainings.models import Category_training, Training


def test_image(name="test.gif"):
    return SimpleUploadedFile(
        name,
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;",
        content_type="image/gif",
    )


class TemporaryMediaTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.media_directory = TemporaryDirectory()
        self.media_override = override_settings(MEDIA_ROOT=self.media_directory.name)
        self.media_override.enable()

    def tearDown(self):
        self.media_override.disable()
        self.media_directory.cleanup()
        super().tearDown()

    def create_category(self, slug="programim"):
        return Category_training.objects.create(
            cat_training_name="Programim",
            cat_training_text_short="Aftësi praktike për zhvillim software.",
            cat_training_img=test_image("category.gif"),
            cat_training_img_alt="Ikonë programimi",
            cat_training_icon="fas fa-code",
            cat_slug=slug,
        )


class HomepageTests(TemporaryMediaTestCase):
    def test_homepage_has_modern_content_and_complete_seo(self):
        category = self.create_category()
        Partner.objects.create(
            partner_name="Partner Test",
            partner_logo=test_image("partner.gif"),
            partner_image_alt="Partner Test",
        )

        response = self.client.get(reverse("home"))
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('<html lang="sq">', html)
        self.assertEqual(len(re.findall(r"<h1(?:\s|>)", html)), 1)
        self.assertContains(response, "Aftësi për karrierën.")
        self.assertContains(response, 'rel="canonical" href="https://dominusoft.al/"')
        self.assertContains(response, "og-dominusoft-home.png")
        self.assertContains(response, reverse("training_category"))
        self.assertContains(response, reverse("services"))
        self.assertContains(response, reverse("trainings", args=[category.cat_slug]))
        self.assertContains(response, 'aria-current="page"')
        self.assertNotContains(response, "typed.umd.js")
        self.assertNotContains(response, "owl.carousel.min.js")

        structured_data_match = re.search(
            r'<script id="homepage-structured-data" type="application/ld\+json">(.*?)</script>',
            html,
            re.DOTALL,
        )
        self.assertIsNotNone(structured_data_match)
        structured_data = json.loads(structured_data_match.group(1))
        structured_types = {item["@type"] for item in structured_data["@graph"]}
        self.assertEqual(structured_types, {"WebSite", "EducationalOrganization"})

    def test_homepage_uses_configurable_training_icons(self):
        category = self.create_category()
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fas fa-code")
        self.assertContains(response, reverse("trainings", args=[category.cat_slug]))

    def test_homepage_hides_empty_dynamic_sections(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="courses-title"')
        self.assertNotContains(response, 'id="partners-title"')
        self.assertContains(response, 'id="services-title"')


class SearchTests(TemporaryMediaTestCase):
    def setUp(self):
        super().setUp()
        category = self.create_category()
        self.training = Training.objects.create(
            training_name="Python Profesional",
            training_text="Program praktik Python.",
            training_image=test_image("python.gif"),
            training_image_alt="Kurs Python",
            training_category=category,
            training_slug="python-profesional",
        )
        self.article = Article.objects.create(
            article_slug="python-artikel",
            article_title="Python në praktikë",
            article_excerpt="Artikull për Python dhe automatizim.",
            article_image=test_image("article.gif"),
            article_image_alt="Python në praktikë",
            article_infos="<p>Një artikull mbi Python dhe automatizim.</p>",
        )
        self.service = Services.objects.create(
            services_name="Zgjidhje Python",
            services_description="Krijim aplikacionesh me Python dhe automatizim.",
            services_image=test_image("service.gif"),
            services_alt="Python",
        )

    def test_get_search_is_case_insensitive_and_noindex(self):
        response = self.client.get(reverse("searchvenues"), {"q": "python"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.training.training_name)
        self.assertContains(response, self.article.article_title)
        self.assertContains(response, self.service.services_name)
        self.assertContains(response, '<meta name="robots" content="noindex,follow">')
        self.assertEqual(response.context["searched"], "python")

    def test_empty_get_search_shows_prompt(self):
        response = self.client.get(reverse("searchvenues"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Çfarë dëshironi të mësoni?")
        self.assertNotContains(response, self.training.training_name)

    def test_legacy_post_redirects_to_shareable_get_url(self):
        response = self.client.post(reverse("searchvenues"), {"search": "Python Profesional"})

        self.assertRedirects(
            response,
            f'{reverse("searchvenues")}?q=Python+Profesional',
            fetch_redirect_response=False,
        )


class ArticleSchedulingTests(TemporaryMediaTestCase):
    def test_article_status_supports_draft_and_scheduled_publish(self):
        now = timezone.now()
        published = Article.objects.create(
            article_slug="published-article",
            article_title="Published article",
            article_image=test_image("published.gif"),
            article_status=Article.ArticleStatus.PUBLISHED,
        )
        draft = Article.objects.create(
            article_slug="draft-article",
            article_title="Draft article",
            article_image=test_image("draft.gif"),
            article_status=Article.ArticleStatus.DRAFT,
        )
        scheduled = Article.objects.create(
            article_slug="scheduled-article",
            article_title="Scheduled article",
            article_image=test_image("scheduled.gif"),
            article_status=Article.ArticleStatus.SCHEDULED,
            article_publish_at=now + timedelta(days=1),
        )

        self.assertTrue(published.is_published)
        self.assertFalse(draft.is_published)
        self.assertFalse(scheduled.is_published)
        self.assertEqual(Article.ArticleStatus.choices[0][0], "draft")


class SubscribeTests(TestCase):
    def test_valid_subscription_normalizes_email_and_returns_to_footer(self):
        response = self.client.post(
            reverse("subscribe"),
            {"subscribe_email": " USER@Example.COM ", "next": reverse("blog")},
        )

        self.assertRedirects(
            response,
            f'{reverse("blog")}#subscribe',
            fetch_redirect_response=False,
        )
        self.assertTrue(Subscribe.objects.filter(subscribe_email="user@example.com").exists())

    def test_duplicate_subscription_does_not_create_another_record(self):
        Subscribe.objects.create(subscribe_email="user@example.com")
        response = self.client.post(
            reverse("subscribe"),
            {"subscribe_email": "USER@example.com", "next": reverse("home")},
        )
        messages = [str(message) for message in get_messages(response.wsgi_request)]

        self.assertEqual(Subscribe.objects.count(), 1)
        self.assertIn("Kjo adresë është abonuar më parë. Faleminderit!", messages)

    def test_invalid_subscription_is_rejected(self):
        response = self.client.post(
            reverse("subscribe"),
            {"subscribe_email": "jo-email", "next": reverse("home")},
        )

        self.assertEqual(Subscribe.objects.count(), 0)
        self.assertEqual(response.status_code, 302)

    def test_external_return_url_is_rejected(self):
        response = self.client.post(
            reverse("subscribe"),
            {"subscribe_email": "user@example.com", "next": "https://example.org/phishing"},
        )

        self.assertEqual(response["Location"], f'{reverse("home")}#subscribe')

    def test_subscription_is_post_only_and_csrf_protected(self):
        self.assertEqual(self.client.get(reverse("subscribe")).status_code, 405)
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(
            reverse("subscribe"),
            {"subscribe_email": "user@example.com"},
        )
        self.assertEqual(response.status_code, 403)


class DiscoveryAndShellTests(TemporaryMediaTestCase):
    def test_robots_and_dynamic_sitemap(self):
        category = self.create_category(slug="programim-web")
        training = Training.objects.create(
            training_name="Web Development",
            training_category=category,
            training_slug="web-development",
        )
        article = Article.objects.create(
            article_slug="seo-modern",
            article_title="SEO modern",
            article_image=test_image("article.gif"),
        )

        robots_response = self.client.get(reverse("robots_txt"))
        sitemap_response = self.client.get("/sitemap.xml")

        self.assertEqual(robots_response.status_code, 200)
        self.assertEqual(robots_response["Content-Type"], "text/plain; charset=utf-8")
        self.assertContains(robots_response, "Sitemap: https://dominusoft.al/sitemap.xml")
        self.assertContains(
            sitemap_response,
            reverse("trainings", args=[category.cat_slug]),
        )
        self.assertContains(
            sitemap_response,
            reverse("curricula", args=[category.cat_slug, training.training_slug]),
        )
        self.assertContains(sitemap_response, reverse("article", args=[article.article_slug]))

    def test_public_pages_receive_shared_navigation_and_footer(self):
        public_urls = [
            reverse("home"),
            reverse("services"),
            reverse("training_category"),
            reverse("blog"),
            reverse("student"),
            reverse("business"),
            reverse("career"),
            reverse("policy"),
            reverse("terms"),
            reverse("searchvenues"),
        ]

        for url in public_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'class="site-header')
                self.assertContains(response, 'class="site-footer"')
                self.assertContains(response, reverse("subscribe"))
