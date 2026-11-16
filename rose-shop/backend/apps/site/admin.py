from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            'Contact & social',
            {
                'fields': ('phone', 'instagram', 'tiktok'),
                'description': (
                    'Phone, Instagram and TikTok shown in the footer, contact page and menu. '
                    'For social: username only (e.g. finessia.al), without @.'
                ),
            },
        ),
        (
            'Page images',
            {
                'fields': ('about_image', 'contact_image', 'updated_at'),
            },
        ),
    )
    readonly_fields = ['updated_at']

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def changelist_view(self, request, extra_context=None):
        SiteSettings.load()
        return redirect(reverse('admin:site_sitesettings_change', args=(1,)))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        SiteSettings.load()
        return super().change_view(request, '1', form_url, extra_context)
