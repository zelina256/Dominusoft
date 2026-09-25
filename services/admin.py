from django.contrib import admin

from .models import (
    ServiceBenefit,
    ServiceDetail,
    ServiceHighlight,
    ServicePackage,
    ServicePackageItem,
    ServiceProject,
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


class ServiceProjectInline(admin.StackedInline):
    model = ServiceProject
    extra = 1


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = (
        'services_name', 'services_icon',
    )
    search_fields = ('services_name', 'services_title', 'services_icon', 'slug')
    list_filter = ('services_name',)
    inlines = [
        ServiceHighlightInline,
        ServiceBenefitInline,
        ServicePackageInline,
        ServiceProjectInline,
    ]


@admin.register(ServiceDetail)
class ServiceDetailAdmin(admin.ModelAdmin):
    list_display = (
       'service', 'eyebrow', 'title', 'lead', 'summary',
        'summary_additional',
    )
    list_filter = ('is_active',)
    search_fields = ('title', 'service__services_name')


@admin.register(ServiceHighlight)
class ServiceHighlightAdmin(admin.ModelAdmin):
    list_display = ('service', 'title', 'description', 'order')
    list_filter = ('service',)
    search_fields = ('title', 'service__services_name')


@admin.register(ServiceBenefit)
class ServiceBenefitAdmin(admin.ModelAdmin):
    list_display = ('service', 'title', 'description', 'icon', 'order')
    list_filter = ('service',)
    search_fields = ('title', 'service__services_name')


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = (
        'service', 'name', 'price', 'description', 'is_featured', 'order',
    )
    list_filter = ('service', 'is_featured')
    search_fields = ('name', 'service__services_name')
    inlines = [ServicePackageItemInline]


@admin.register(ServicePackageItem)
class ServicePackageItemAdmin(admin.ModelAdmin):
    list_display = ('package', 'text', 'order')
    list_filter = ('package',)
    search_fields = ('text', 'package__name')


@admin.register(ServiceProject)
class ServiceProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'is_published', 'order')
    list_filter = ('service', 'is_published')
    search_fields = ('title', 'description', 'service__services_name')
    ordering = ('service', 'order', 'id')
