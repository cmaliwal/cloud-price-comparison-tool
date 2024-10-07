from .providers.aws_provider import AWSProvider

class CloudPricingAPI:
    def __init__(self):
        self.providers = {
            "aws": AWSProvider(),
            # You can add more providers like Azure, Google, etc.
        }

    def get_all_prices(self):
        all_prices = []

        # Loop through each cloud provider in the providers dictionary
        for provider_name, provider_instance in self.providers.items():
            print(f"Fetching prices for provider: {provider_name}")

            # Loop through the regions of the current provider
            for region in provider_instance.regions:
                print(f"Fetching prices for {provider_name} region: {region}")
                prices = provider_instance.get_prices(region=region)

                # If prices are fetched, extend the all_prices list
                if prices:
                    all_prices.extend(prices)

        return all_prices
