from django.urls import path, reverse_lazy
from . import views

app_name = "register"

urlpatterns = [
    path("new/", views.register, name="user_create"),
    path("", views.UserListView.as_view()),
    path("view/", views.UserListView.as_view(), name="user_view"),
    path("update/<int:pk>", views.UserUpdateView.as_view(), name="user_update"),
    path("delete/<int:pk>", views.UserDeleteView.as_view(), name="user_delete"),
]
