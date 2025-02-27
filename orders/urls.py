from django.urls import path, reverse_lazy

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path(
        "create/",
        views.OrderCreateView.as_view(success_url="/view/order/"),
        name="order_create",
    ),
    path("view/", views.OrderListView.as_view(), name="view"),
    path("view/order/<int:pk>", views.OrderDetailView.as_view(), name="order_detail"),
    path("delete/<int:pk>", views.OrderDeleteView.as_view(), name="order_delete"),
    path(
        "update_pay/<int:pk>",
        views.OrderUpdatePaymentView.as_view(),
        name="order_update_pay",
    ),
    path(
        "update_delivery/<int:pk>",
        views.OrderUpdateDeliveryView.as_view(),
        name="order_update_delivery",
    ),
    # path("details/", views.ShopUpdateView.as_view(success_url = reverse_lazy('home')), name = "shop"),
]
