from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Testimonial)
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
	list_display = (
		"partner_name",
	)
	search_fields = ("partner_name", "partner_image_alt")
