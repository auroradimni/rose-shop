from django.contrib import admin
from django import forms

from .models import CustomerReview


class CustomerReviewAdminForm(forms.ModelForm):
    class Meta:
        model = CustomerReview
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['is_published'].initial = True


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    form = CustomerReviewAdminForm
    list_display = ['review_label', 'image_thumb', 'text_preview', 'is_published', 'order', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['username', 'text']
    list_editable = ['is_published', 'order']
    readonly_fields = ['created_at']
    ordering = ['order', '-created_at']

    @admin.display(description='Review')
    def review_label(self, obj):
        return str(obj)

    @admin.display(description='Photo')
    def image_thumb(self, obj):
        if obj.image:
            return obj.image.name
        return '—'

    @admin.display(description='Comment')
    def text_preview(self, obj):
        if not obj.text:
            return '—'
        return obj.text[:60] + ('…' if len(obj.text) > 60 else '')
