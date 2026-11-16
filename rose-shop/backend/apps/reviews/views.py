from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomerReview
from .serializers import CustomerReviewSerializer, CustomerReviewSubmitSerializer


class PublishedReviewListView(APIView):
    def get(self, request):
        qs = CustomerReview.objects.filter(is_published=True)
        serializer = CustomerReviewSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)


class CustomerReviewSubmitView(APIView):
    throttle_scope = 'reviews'

    def post(self, request):
        serializer = CustomerReviewSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            {
                'message': (
                    'Thank you! Your review was received and will appear on the site '
                    'after our team approves it.'
                ),
            },
            status=status.HTTP_201_CREATED,
        )
