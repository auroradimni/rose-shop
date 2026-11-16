from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NewsletterSubscriber


class SubscriptionSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)


class SubscribeView(APIView):
    throttle_scope = 'newsletter'

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _, created = NewsletterSubscriber.objects.get_or_create(
            email=serializer.validated_data['email'].lower(),
        )
        return Response({'message': 'Subscribed successfully!' if created else 'Already subscribed.'})
