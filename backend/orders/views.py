from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Cart, CartItem, Order, OrderItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
)
from products.models import Product


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        # Temporary user for API testing.
        # Authentication will be added later.
        cart, created = Cart.objects.get_or_create(
            user_id=1
        )
        return cart


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product")
        quantity = request.data.get("quantity", 1)

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True
        )

        cart, created = Cart.objects.get_or_create(
            user_id=1
        )

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not item_created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = self.get_serializer(cart_item)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class UpdateCartItemView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user_id=1
        )

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()

        quantity = request.data.get("quantity")

        if quantity is None:
            return Response(
                {"error": "Quantity is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        quantity = int(quantity)

        if quantity < 1:
            return Response(
                {"error": "Quantity must be at least 1."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()

        serializer = self.get_serializer(cart_item)

        return Response(serializer.data)


class RemoveCartItemView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user_id=1
        )


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Order.objects.filter(
            user_id=1
        ).order_by("-created_at")


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Order.objects.filter(
            user_id=1
        )


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        cart = get_object_or_404(
            Cart,
            user_id=1
        )

        cart_items = cart.items.select_related(
            "product"
        )

        if not cart_items.exists():
            return Response(
                {"error": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        delivery_address = request.data.get(
            "delivery_address"
        )

        phone_number = request.data.get(
            "phone_number"
        )

        notes = request.data.get(
            "notes",
            ""
        )

        if not delivery_address or not phone_number:
            return Response(
                {
                    "error": (
                        "Delivery address and phone number "
                        "are required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        total_amount = sum(
            item.product.current_price * item.quantity
            for item in cart_items
        )

        order = Order.objects.create(
            user_id=1,
            order_number=self.generate_order_number(),
            total_amount=total_amount,
            delivery_address=delivery_address,
            phone_number=phone_number,
            notes=notes,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.current_price,
            )

            item.product.stock_quantity -= item.quantity
            item.product.save()

        cart.items.all().delete()

        serializer = self.get_serializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def generate_order_number(self):
        import uuid

        return f"ORD-{uuid.uuid4().hex[:10].upper()}"