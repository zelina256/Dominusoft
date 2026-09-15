from django.db import models
from django.utils.text import slugify


class Services(models.Model):
    services_id = models.AutoField(primary_key=True)
    services_name = models.CharField(max_length=100, null=True, blank=True)
    services_description = models.TextField(max_length=1000, null=True, blank=True)
    services_meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    services_meta_description = models.CharField(max_length=250, null=True, blank=True)
    services_title = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def _generate_unique_slug(self, base_slug):
        candidate = base_slug or f'service-{self.services_id or "new"}'
        candidate = candidate[:150]
        suffix = 1
        queryset = Services.objects.filter(slug=candidate).exclude(pk=self.pk)

        while queryset.exists():
            suffix_text = f'-{suffix}'
            candidate = f"{base_slug[:150 - len(suffix_text)]}{suffix_text}" if base_slug else f"service-{self.services_id or 'new'}-{suffix}"
            queryset = Services.objects.filter(slug=candidate).exclude(pk=self.pk)
            suffix += 1

        return candidate

    def save(self, *args, **kwargs):
        if self.services_name:
            base_slug = slugify(self.services_name)
            if not self.slug or self.slug == slugify(self.services_name):
                self.slug = self._generate_unique_slug(base_slug)
        elif not self.slug:
            self.slug = self._generate_unique_slug(f"service-{self.services_id or 'new'}")
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.services_name or self.services_title or self.services_id)


class ServiceDetail(models.Model):
    service = models.OneToOneField(
        Services,
        on_delete=models.CASCADE,
        related_name='detail'
    )
    eyebrow = models.CharField(max_length=80, default='Sherbimi')
    title = models.CharField(max_length=200)
    lead = models.TextField(max_length=500)
    summary = models.TextField(max_length=1500)
    summary_additional = models.TextField(max_length=1500, blank=True, null=True)
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(max_length=250, blank=True, null=True)
    canonical_url = models.CharField(max_length=250, blank=True, null=True)
    cta_text = models.CharField(max_length=100, default='Rezervo konsultë')
    cta_url = models.CharField(max_length=255, default='#rezervo')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ServiceHighlight(models.Model):
    service = models.ForeignKey(
        Services,
        related_name='highlights',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.service} - {self.title}'


class ServiceBenefit(models.Model):
    service = models.ForeignKey(
        Services,
        related_name='benefits',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500)
    icon = models.CharField(max_length=50, default='fa-check-circle')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.service} - {self.title}'


class ServicePackage(models.Model):
    service = models.ForeignKey(
        Services,
        related_name='packages',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=120)
    price = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=800, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.service} - {self.name}'


class ServicePackageItem(models.Model):
    package = models.ForeignKey(
        ServicePackage,
        related_name='items',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=250)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.text
