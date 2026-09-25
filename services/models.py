from django.db import models
from django.utils.text import slugify


class Services(models.Model):
    services_id = models.AutoField(primary_key=True)
    services_name = models.CharField(max_length=100, null=True, blank=True)
    services_description = models.TextField(max_length=1000, null=True, blank=True)
    services_meta_keyword = models.CharField(max_length=250, null=True, blank=True)
    services_meta_description = models.CharField(max_length=250, null=True, blank=True)
    services_title = models.CharField(max_length=250, null=True, blank=True)
    services_icon = models.CharField(
        max_length=80,
        default='fas fa-laptop-code',
        help_text="Font Awesome class, p.sh. 'fas fa-globe' ose 'fas fa-chart-line'.",
    )
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def _generate_unique_slug(self, base_slug):
        base = (base_slug or 'service')[:150]
        candidate = base
        suffix = 1
        while type(self).objects.filter(slug=candidate).exclude(pk=self.pk).exists():
            ending = f'-{suffix}'
            candidate = f'{base[:150 - len(ending)]}{ending}'
            suffix += 1
        return candidate

    def save(self, *args, **kwargs):
        # A published URL remains stable when the visible name changes.
        if not self.slug:
            self.slug = self._generate_unique_slug(slugify(self.services_name or '') or 'service')
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.services_name or self.services_title or self.services_id)


class ServiceDetail(models.Model):
    service = models.OneToOneField(Services, on_delete=models.CASCADE, related_name='detail')
    eyebrow = models.CharField(max_length=80, default='Shërbimi')
    title = models.CharField(max_length=200)  # H1: one per page
    lead = models.TextField(max_length=500)
    summary = models.TextField(max_length=1500)
    summary_additional = models.TextField(max_length=1500, blank=True, null=True)
    hero_panel_title = models.CharField(max_length=120, blank=True, null=True)
    why_section_title = models.CharField(max_length=200, blank=True, null=True)  # H2
    why_section_subtitle = models.CharField(max_length=200, blank=True, null=True)  # H3
    why_section_body = models.TextField(blank=True)
    benefits_section_title = models.CharField(max_length=200, blank=True, null=True)  # H2
    benefits_intro = models.TextField(blank=True)
    packages_section_title = models.CharField(max_length=200, blank=True, null=True)  # H2
    projects_section_title = models.CharField(max_length=200, blank=True, null=True)  # H2
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(max_length=250, blank=True, null=True)
    canonical_url = models.CharField(max_length=250, blank=True, null=True)
    cta_text = models.CharField(max_length=100, default='Rezervo konsultë')
    cta_url = models.CharField(max_length=255, default='#rezervo')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ServiceHighlight(models.Model):
    service = models.ForeignKey(Services, related_name='highlights', on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.service} - {self.title}'


class ServiceBenefit(models.Model):
    service = models.ForeignKey(Services, related_name='benefits', on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500)
    icon = models.CharField(max_length=50, default='fa-check-circle')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.service} - {self.title}'


class ServicePackage(models.Model):
    service = models.ForeignKey(Services, related_name='packages', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)  # H3
    price = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=800, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.service} - {self.name}'


class ServicePackageItem(models.Model):
    package = models.ForeignKey(ServicePackage, related_name='items', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.text


class ServiceProject(models.Model):
    service = models.ForeignKey(Services, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    image = models.ImageField(upload_to='service_projects/', blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class ServiceOffering(models.Model):
    """Optional individual services, separate from priced/quoted packages."""
    service = models.ForeignKey(Services, related_name='offerings', on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title