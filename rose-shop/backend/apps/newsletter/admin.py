# apps/newsletter/admin.py
from django.contrib import admin
from .models import NewsletterSubscriber

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']
    readonly_fields = ['email', 'created_at']
