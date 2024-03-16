from rest_framework import generics

from shop import models
from shop import serializers
from shop.permissions import HasPermissionToDestroy


class CartListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartReadSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.id)

    def get_serializer(self, *args, **kwargs):

        if self.request.method == "POST":
            return serializers.CartCreateSerializer(*args, **kwargs)

        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartDestroyAPIView(generics.DestroyAPIView):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartReadSerializer

    permission_classes = (HasPermissionToDestroy,)


class CheckoutListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Checkout.objects.all()
    serializer_class = serializers.CheckoutSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.id)

    def get_serializer(self, *args, **kwargs):

        if self.request.method == "POST":
            return serializers.CheckoutCreateSerializer(*args, **kwargs)

        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
