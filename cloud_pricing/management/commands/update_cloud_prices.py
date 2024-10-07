from django.core.management.base import BaseCommand
from django.db import transaction

from cloud_pricing.models import CloudInstancePrice
from cloud_pricing.services import CloudPricingAPI


class Command(BaseCommand):
    help = "Update cloud instance prices from various providers"

    def handle(self, *args, **kwargs):
        try:
            pricing_api = CloudPricingAPI()
            prices = pricing_api.get_all_prices()
            instances_to_update = []
            instances_to_create = []
            unique_fields_set = set()

            for price_data in prices:
                unique_fields = (
                    price_data["cloud_type"],
                    price_data["location"],
                    price_data["instance_type"],
                    price_data["instance_family"],
                    price_data["vcpu"],
                    price_data["ram_gb"],
                )

                # Check if this unique combination exists in the database
                instance = CloudInstancePrice.objects.filter(
                    cloud_type=price_data["cloud_type"],
                    location=price_data["location"],
                    instance_type=price_data["instance_type"],
                    instance_family=price_data["instance_family"],
                    vcpu=price_data["vcpu"],
                    ram_gb=price_data["ram_gb"],
                ).first()

                if instance:
                    # Update the existing instance
                    instance.effective_date = price_data["effective_date"]
                    instance.price_per_hour = price_data["price_per_hour"]
                    instances_to_update.append(instance)
                else:
                    # Create a new instance
                    instance = CloudInstancePrice(
                        cloud_type=price_data["cloud_type"],
                        location=price_data["location"],
                        instance_type=price_data["instance_type"],
                        instance_family=price_data["instance_family"],
                        vcpu=price_data["vcpu"],
                        ram_gb=price_data["ram_gb"],
                        effective_date=price_data["effective_date"],
                        price_per_hour=price_data["price_per_hour"],
                    )
                    instances_to_create.append(instance)

                unique_fields_set.add(unique_fields)

            # Use bulk operations for efficiency
            with transaction.atomic():
                if instances_to_create:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Creating {len(instances_to_create)} instances..."
                        )
                    )
                    CloudInstancePrice.objects.bulk_create(instances_to_create)

                if instances_to_update:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Updating {len(instances_to_update)} instances..."
                        )
                    )
                    CloudInstancePrice.objects.bulk_update(
                        instances_to_update,
                        ["effective_date", "price_per_hour"],
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully updated cloud instance prices."
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to update cloud instance prices. Error: {e}"
                )
            )
