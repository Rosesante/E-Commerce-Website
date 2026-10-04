from django.urls import path

from .views import (
    CartView,
    AddToCartView,
    UpdateCartItemView,
    RemoveCartItemView,
    OrderListView,
    OrderDetailView,
    CreateOrderView,
)


urlpatterns = [
    # Cart
    path(
        "cart/",
        CartView.as_view(),
        name="cart"
    ),

    path(
        "cart/add/",
        AddToCartView.as_view(),
        name="cart-add"
    ),

    path(
        "cart/item/<int:pk>/update/",
        UpdateCartItemView.as_view(),
        name="cart-item-update"
    ),

    path(
        "cart/item/<int:pk>/remove/",
        RemoveCartItemView.as_view(),
        name="cart-item-remove"
    ),

    # Orders
    path(
        "",
        OrderListView.as_view(),
        name="order-list"
    ),

    path(
        "create/",
        CreateOrderView.as_view(),
        name="order-create"
    ),

    path(
        "<int:pk>/",
        OrderDetailView.as_view(),
        name="order-detail"
    ),
]