from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("trainings", "0016_auto_20260831_1844"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoryPageContent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("summary_title", models.CharField(blank=True, max_length=250)),
                ("certification_title", models.CharField(blank=True, max_length=250)),
                ("learning_title", models.CharField(blank=True, max_length=250)),
                ("learning_description", models.TextField(blank=True)),
                ("faq_title", models.CharField(blank=True, max_length=250)),
                ("category", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="page_content", to="trainings.category_training")),
            ],
        ),
        migrations.CreateModel(
            name="CategoryHighlight",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("description", models.TextField(max_length=500)),
                ("order", models.PositiveIntegerField(default=0)),
                ("content", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="highlights", to="trainings.categorypagecontent")),
            ],
            options={"ordering": ["order", "id"]},
        ),
        migrations.CreateModel(
            name="CategoryCertificationItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=300)),
                ("order", models.PositiveIntegerField(default=0)),
                ("content", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="certification_items", to="trainings.categorypagecontent")),
            ],
            options={"ordering": ["order", "id"]},
        ),
        migrations.CreateModel(
            name="CategoryFaq",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question", models.CharField(max_length=300)),
                ("answer", models.TextField(max_length=1000)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_open", models.BooleanField(default=False)),
                ("content", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="faqs", to="trainings.categorypagecontent")),
            ],
            options={"ordering": ["order", "id"]},
        ),
    ]
