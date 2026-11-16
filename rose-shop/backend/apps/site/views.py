from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SiteSettings
from .serializers import SiteSettingsSerializer


class SiteSettingsView(APIView):
    """Public site content (about image, etc.)."""

    def get(self, request):
        settings = SiteSettings.load()
        serializer = SiteSettingsSerializer(settings, context={'request': request})
        return Response(serializer.data)
