from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('home/', views.home, name = "home"),
    path("create/", views.OrderUpdateView.as_view(success_url = reverse_lazy('view')), name = "create"),
    path("view/", views.view, name = "view"),
    # path("details/", views.ShopUpdateView.as_view(success_url = reverse_lazy('home')), name = "shop"),
]