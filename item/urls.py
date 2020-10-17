from django.urls import path, reverse_lazy
from . import views

app_name = "item"

urlpatterns = [
    path("create/", views.ItemCreateView.as_view(), name = "item_create"),
    path("view/", views.ItemListView.as_view(), name = "item_view"),
    path("update/<int:pk>", views.ItemUpdateView.as_view(), name = "item_update"),
    path("delete/<int:pk>", views.ItemDeleteView.as_view(), name = "item_delete"),
]