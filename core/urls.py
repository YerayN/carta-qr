from django.urls import path
from .views_api import HelloView

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
]
