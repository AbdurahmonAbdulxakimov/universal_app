from rest_framework import serializers

from shop import models


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = "__all__"


class ProductCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = "__all__"


class CartReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer()

    class Meta:
        model = models.Cart
        fields = ("id", "user", "product", "amount", "price", "updated_at")


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ("id", "product", "amount", "updated_at")


class CheckoutSerializer(serializers.ModelSerializer):
    carts = CartReadSerializer(many=True, read_only=True)
    total_price = serializers.IntegerField(allow_null=True)

    class Meta:
        model = models.Checkout
        fields = "__all__"


class CheckoutCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Checkout
        exclude = ("user",)

    def create(self, validated_data):
        total_price = 0
        for cart in validated_data["carts"]:
            total_price += cart.price

        validated_data["total_price"] = (
            validated_data["promotional_discount"]
            + validated_data["shipping_fee"]
            + total_price
        )
        return super().create(validated_data)
