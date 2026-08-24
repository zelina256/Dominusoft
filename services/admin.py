from django.contrib import admin

from .models import (
    RelatedService,
    ServiceBenefit,
    ServiceDetail,
    ServiceFaq,
    ServiceHighlight,
    ServicePackage,
    ServicePackageItem,
    Services,
)


class ServiceHighlightInline(admin.StackedInline):
    model = ServiceHighlight
    extra = 1


class ServiceBenefitInline(admin.StackedInline):
    model = ServiceBenefit
    extra = 1


class ServicePackageItemInline(admin.StackedInline):
    model = ServicePackageItem
    extra = 1


class ServicePackageInline(admin.StackedInline):
    model = ServicePackage
    extra = 1
    inlines = [ServicePackageItemInline]


class ServiceFaqInline(admin.StackedInline):
    model = ServiceFaq
    extra = 1


class RelatedServiceInline(admin.StackedInline):
    model = RelatedService
    fk_name = 'service'
    extra = 1


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('services_name', 'services_title', 'slug')
    search_fields = ('services_name', 'services_title', 'slug')
    list_filter = ('services_name',)
    inlines = [
        ServiceHighlightInline,
        ServiceBenefitInline,
        ServiceFaqInline,
        ServicePackageInline,
        RelatedServiceInline,
    ]


@admin.register(ServiceDetail)
class ServiceDetailAdmin(admin.ModelAdmin):
    list_display = ('service', 'title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'service__services_name')


@admin.register(ServiceHighlight)
class ServiceHighlightAdmin(admin.ModelAdmin):
    list_display = ('service', 'title', 'order')
    list_filter = ('service',)
    search_fields = ('title', 'service__services_name')


@admin.register(ServiceBenefit)
class ServiceBenefitAdmin(admin.ModelAdmin):
    list_display = ('service', 'title', 'icon', 'order')
    list_filter = ('service',)
    search_fields = ('title', 'service__services_name')


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ('service', 'name', 'price', 'is_featured', 'order')
    list_filter = ('service', 'is_featured')
    search_fields = ('name', 'service__services_name')
    inlines = [ServicePackageItemInline]


@admin.register(ServicePackageItem)
class ServicePackageItemAdmin(admin.ModelAdmin):
    list_display = ('package', 'text', 'order')
    list_filter = ('package',)
    search_fields = ('text', 'package__name')


@admin.register(ServiceFaq)
class ServiceFaqAdmin(admin.ModelAdmin):
    list_display = ('service', 'question', 'is_open', 'order')
    list_filter = ('service', 'is_open')
    search_fields = ('question', 'service__services_name')


@admin.register(RelatedService)
class RelatedServiceAdmin(admin.ModelAdmin):
    list_display = ('service', 'related', 'title', 'order')
    list_filter = ('service',)
    search_fields = ('title', 'service__services_name', 'related__services_name')
