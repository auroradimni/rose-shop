from rest_framework import serializers

from config.media_urls import media_absolute_url
from .models import CustomerReview


class CustomerReviewSerializer(serializers.ModelSerializer):
    """Public list — photo + comment (no customer name)."""

    image = serializers.SerializerMethodField()

    class Meta:
        model = CustomerReview
        fields = ['id', 'text', 'image']

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        return media_absolute_url(request, obj.image)


class CustomerReviewSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReview
        fields = ['image', 'text']

    def validate_image(self, value):
        if value.size > 8 * 1024 * 1024:
            raise serializers.ValidationError('Image must be 8 MB or smaller.')
        return value

    def create(self, validated_data):
        return CustomerReview.objects.create(
            **validated_data,
            username='',
            is_published=False,
        )
