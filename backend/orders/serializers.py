from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_price = serializers.DecimalField(
        source="product.current_price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "quantity",
            "subtotal",
        ]

    def get_subtotal(self, obj):
        return obj.product.current_price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(
        many=True,
        read_only=True
    )

    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total",
            "created_at",
            "updated_at",
        ]

    def get_total(self, obj):
        return sum(
            item.product.current_price * item.quantity
            for item in obj.items.all()
        )


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "price",
            "subtotal",
        ]

    def get_subtotal(self, obj):
        return obj.price * obj.quantity


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "total_amount",
            "delivery_address",
            "phone_number",
            "notes",
            "items",
            "created_at",
            "updated_at",
        ]