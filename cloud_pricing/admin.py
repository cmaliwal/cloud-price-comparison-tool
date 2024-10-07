from django.contrib import admin

from .models import CloudInstancePrice


@admin.register(CloudInstancePrice)
class CloudInstancePriceAdmin(admin.ModelAdmin):
    list_display = (
        "cloud_type",
        "location",
        "instance_type",
        "vcpu",
        "ram_gb",
        "price_per_hour",
        "effective_date",
    )
    list_filter = ("cloud_type", "location", "effective_date")
    search_fields = ("instance_type", "instance_family")
