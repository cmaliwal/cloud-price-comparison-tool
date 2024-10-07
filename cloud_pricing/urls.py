from django.urls import path

from .views import CloudInstancePriceList

urlpatterns = [
    path(
        "cloud-instances/",
        CloudInstancePriceList.as_view(),
        name="cloud-instance-list",
    ),
]
