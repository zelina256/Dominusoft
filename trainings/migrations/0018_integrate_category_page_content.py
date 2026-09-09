from django.db import migrations, models
import django.db.models.deletion


def move_content_to_category(apps, schema_editor):
    CategoryTraining = apps.get_model("trainings", "Category_training")
    CategoryPageContent = apps.get_model("trainings", "CategoryPageContent")
    CategoryHighlight = apps.get_model("trainings", "CategoryHighlight")
    CategoryCertificationItem = apps.get_model("trainings", "CategoryCertificationItem")
    CategoryFaq = apps.get_model("trainings", "CategoryFaq")

    for content in CategoryPageContent.objects.all():
        CategoryTraining.objects.filter(pk=content.category_id).update(
            category_summary_title=content.summary_title,
            category_certification_title=content.certification_title,
            category_learning_title=content.learning_title,
            category_learning_description=content.learning_description,
            category_faq_title=content.faq_title,
        )
        CategoryHighlight.objects.filter(content_id=content.pk).update(
            category_id=content.category_id
        )
        CategoryCertificationItem.objects.filter(content_id=content.pk).update(
            category_id=content.category_id
        )
        CategoryFaq.objects.filter(content_id=content.pk).update(
            category_id=content.category_id
        )


class Migration(migrations.Migration):

    dependencies = [
        ("trainings", "0017_category_page_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="category_training",
            name="category_summary_title",
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name="category_training",
            name="category_certification_title",
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name="category_training",
            name="category_learning_title",
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name="category_training",
            name="category_learning_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="category_training",
            name="category_faq_title",
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name="categoryhighlight",
            name="category",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="highlights", to="trainings.category_training"),
        ),
        migrations.AddField(
            model_name="categorycertificationitem",
            name="category",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="certification_items", to="trainings.category_training"),
        ),
        migrations.AddField(
            model_name="categoryfaq",
            name="category",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="faqs", to="trainings.category_training"),
        ),
        migrations.RunPython(move_content_to_category, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="categoryhighlight",
            name="content",
        ),
        migrations.RemoveField(
            model_name="categorycertificationitem",
            name="content",
        ),
        migrations.RemoveField(
            model_name="categoryfaq",
            name="content",
        ),
        migrations.DeleteModel(
            name="CategoryPageContent",
        ),
        migrations.AlterField(
            model_name="categoryhighlight",
            name="category",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="highlights", to="trainings.category_training"),
        ),
        migrations.AlterField(
            model_name="categorycertificationitem",
            name="category",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="certification_items", to="trainings.category_training"),
        ),
        migrations.AlterField(
            model_name="categoryfaq",
            name="category",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="faqs", to="trainings.category_training"),
        ),
    ]
