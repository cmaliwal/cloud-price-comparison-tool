import boto3
import json
from datetime import datetime


class CloudPricingAPI:
    def __init__(self):
        self.providers = {
            "aws": self.get_aws_prices,
            # 'azure': self.get_azure_prices,
            # 'google': self.get_google_prices,
        }

        self.regions = [
            "us-east-1",
            "eu-central-1",
            "ap-south-1",
        ]

    def get_aws_prices(self, region, service_code="AmazonEC2"):
        aws_access_key_id = "AKIAZZ3UAMQCFIXG5OXN"
        aws_secret_access_key = "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"

        client = boto3.client(
            "pricing",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        try:
            response = client.get_products(
                ServiceCode=service_code,
            )
            print(f"Fetching prices for region: {region}. Got data of length: {len(response['PriceList'])}")
            return self.parse_aws_data(response)

        except Exception as e:
            print(f"Error fetching pricing data: {e}")
            return []

    def parse_aws_data(self, response):
        # Parse and return AWS pricing data
        prices = []
        for product in response["PriceList"]:
            product_data = json.loads(product)
            attributes = product_data["product"]["attributes"]
            effective_date_str = product_data.get("publicationDate", "")
            # Parse the effective_date from string to date
            effective_date = (
                datetime.strptime(effective_date_str, "%Y-%m-%dT%H:%M:%SZ").date()
                if effective_date_str
                else None
            )
            ram_str = attributes.get("memory", "0 GiB")
            ram_gb = self.convert_ram_to_gb(ram_str)

            prices.append(
                {
                    "cloud_type": "AWS",
                    "location": attributes.get("location", ""),
                    "instance_type": attributes.get("instanceType", ""),
                    "vcpu": attributes.get("vcpu", 0),
                    "ram_gb": ram_gb,
                    "price_per_hour": self.extract_price(product_data),
                    "effective_date": effective_date,
                    "instance_family": attributes.get("instanceFamily", ""),
                }
            )
        return prices

    def convert_ram_to_gb(self, ram_str):
        # Convert RAM string (e.g., '16 GiB') to float
        if "GiB" in ram_str:
            return float(ram_str.replace(" GiB", "").strip())
        elif "MiB" in ram_str:
            return float(ram_str.replace(" MiB", "").strip()) / 1024.0
        return 0.0

    def extract_price(self, product_data):
        # Extract the price from the pricing dimensions
        try:
            price_dimensions = product_data["pricing"]["terms"]["OnDemand"]
            for key, value in price_dimensions.items():
                return float(value["priceDimensions"][key]["pricePerUnit"]["USD"])
        except KeyError:
            return 0.0

    # def get_all_prices(self):
    #     all_prices = []
    #     for provider in self.providers.values():
    #         all_prices.extend(provider())
    #     return all_prices

    def get_all_prices(self):
        all_prices = []
        for region in self.regions:
            print(f"Fetching prices for region: {region}")
            prices = self.get_aws_prices(region=region)
            all_prices.extend(prices)
        return all_prices
