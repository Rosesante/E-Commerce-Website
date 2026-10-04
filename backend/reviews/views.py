from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        # Temporary user for API testing.
        # Authentication will be added later.
        serializer.save(user_id=1)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Review.objects.all()