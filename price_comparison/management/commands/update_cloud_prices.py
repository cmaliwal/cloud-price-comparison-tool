from django.core.management.base import BaseCommand
from price_comparison.models import CloudInstancePrice
from price_comparison.services import CloudPricingAPI


class Command(BaseCommand):
    help = 'Update cloud instance prices from various providers'

    def handle(self, *args, **kwargs):
        try:
            pricing_api = CloudPricingAPI()
            prices = pricing_api.get_all_prices()
            for price_data in prices:
                unique_fields = {
                    'cloud_type': price_data['cloud_type'],
                    'location': price_data['location'],
                    'instance_type': price_data['instance_type'],
                    'instance_family': price_data['instance_family'],
                    'vcpu': price_data['vcpu'],
                    'ram_gb': price_data['ram_gb'],
                }

                CloudInstancePrice.objects.update_or_create(
                    defaults={
                        'effective_date': price_data['effective_date'],
                        'price_per_hour': price_data['price_per_hour'],
                    },
                    **unique_fields
                )

            self.stdout.write(self.style.SUCCESS('Successfully updated cloud instance prices.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to update cloud instance prices. Error: {e}'))
