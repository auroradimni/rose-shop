from django.urls import path

from .views import CustomerReviewSubmitView, PublishedReviewListView

urlpatterns = [
    path('', PublishedReviewListView.as_view(), name='review-list'),
    path('submit/', CustomerReviewSubmitView.as_view(), name='review-submit'),
]
