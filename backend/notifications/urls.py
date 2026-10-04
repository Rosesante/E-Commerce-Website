from django.urls import path

from .views import (
    NotificationListView,
    NotificationDetailView,
    MarkNotificationReadView,
)


urlpatterns = [
    path(
        "",
        NotificationListView.as_view(),
        name="notification-list"
    ),

    path(
        "<int:pk>/",
        NotificationDetailView.as_view(),
        name="notification-detail"
    ),

    path(
        "<int:pk>/read/",
        MarkNotificationReadView.as_view(),
        name="notification-mark-read"
    ),
]