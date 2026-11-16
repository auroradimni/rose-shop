from rest_framework import serializers

from apps.products.serializers import _absolute_url
from .models import SiteSettings


def _social_username(value: str) -> str:
    return (value or '').strip().lstrip('@')


class SiteSettingsSerializer(serializers.ModelSerializer):
    about_image = serializers.SerializerMethodField()
    contact_image = serializers.SerializerMethodField()
    instagram_url = serializers.SerializerMethodField()
    tiktok_url = serializers.SerializerMethodField()
    instagram_handle = serializers.SerializerMethodField()
    tiktok_handle = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = [
            'about_image',
            'contact_image',
            'phone',
            'instagram',
            'tiktok',
            'instagram_url',
            'tiktok_url',
            'instagram_handle',
            'tiktok_handle',
            'updated_at',
        ]

    def get_about_image(self, obj):
        return _absolute_url(self.context.get('request'), obj.about_image)

    def get_contact_image(self, obj):
        return _absolute_url(self.context.get('request'), obj.contact_image)

    def get_instagram_url(self, obj):
        user = _social_username(obj.instagram)
        return f'https://instagram.com/{user}' if user else ''

    def get_tiktok_url(self, obj):
        user = _social_username(obj.tiktok)
        return f'https://tiktok.com/@{user}' if user else ''

    def get_instagram_handle(self, obj):
        user = _social_username(obj.instagram)
        return f'@{user}' if user else ''

    def get_tiktok_handle(self, obj):
        user = _social_username(obj.tiktok)
        return f'@{user}' if user else ''
