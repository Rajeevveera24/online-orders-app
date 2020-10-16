from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('home/', views.home, name = "home"),
    path("create/", views.OrderCreateView.as_view(success_url = "/view/order/"), name = "order_create"),
    path("view/", views.OrderListView.as_view(), name = "view"),
    path("view/order/<int:pk>", views.OrderDetailView.as_view(), name = "order_detail"),
    # path("update/order/<int:pk>", views.OrderUpdateView.as_view(), name = "order_update"),
    path("item/create/", views.ItemCreateView.as_view(), name = "item_create"),
    path("item/view/", views.ItemListView.as_view(), name = "item_view"),
    # path("details/", views.ShopUpdateView.as_view(success_url = reverse_lazy('home')), name = "shop"),
]