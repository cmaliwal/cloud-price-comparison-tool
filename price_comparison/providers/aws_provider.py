import boto3
import json
from datetime import datetime
from django.conf import settings
from .abstract_cloud_provider import CloudProvider


class AWSProvider(CloudProvider):
    def __init__(self):

        # AWS-specific regions
        self.regions = [
            "us-east-1",
            # Add more regions if necessary
        ]

    def get_prices(self, region, service_code="AmazonEC2"):
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY

        client = boto3.client(
            "pricing",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        try:
            all_prices = []
            next_token = None
            max_attempts = 50

            for i in range(max_attempts):
                print(f"Attempt {i + 1} of {max_attempts}")
                if next_token:
                    response = client.get_products(
                        ServiceCode=service_code,
                        MaxResults=100,
                        NextToken=next_token
                    )
                else:
                    response = client.get_products(
                        ServiceCode=service_code,
                        MaxResults=100
                    )

                prices = self.parse_data(response)
                all_prices.extend(prices)
                print(f"Fetching prices for region: {region}. Got data of length: {len(response['PriceList'])}")

                next_token = response.get('NextToken')
                if not next_token:
                    print("No more pages to fetch. Exiting loop.")
                    break

            print(f"Total prices fetched for region {region}: {len(all_prices)}")
            return all_prices

        except Exception as e:
            print(f"Error fetching pricing data: {e}")
            return []

    def parse_data(self, response):
        prices = []
        for product in response["PriceList"]:
            product_data = json.loads(product)
            attributes = product_data["product"]["attributes"]
            effective_date_str = product_data.get("publicationDate", "")
            effective_date = (
                datetime.strptime(effective_date_str, "%Y-%m-%dT%H:%M:%SZ").date()
                if effective_date_str
                else None
            )
            ram_str = attributes.get("memory", "0 GiB")
            ram_gb = self.convert_ram_to_gb(ram_str)

            prices.append({
                "cloud_type": "AWS",
                "location": attributes.get("location", ""),
                "instance_type": attributes.get("instanceType", ""),
                "vcpu": attributes.get("vcpu", 0),
                "ram_gb": ram_gb,
                "price_per_hour": self.extract_price(product_data),
                "effective_date": effective_date,
                "instance_family": attributes.get("instanceFamily", ""),
            })
        return prices

    def convert_ram_to_gb(self, ram_str):
        if "GiB" in ram_str:
            return float(ram_str.replace(" GiB", "").strip())
        elif "MiB" in ram_str:
            return float(ram_str.replace(" MiB", "").strip()) / 1024.0
        return 0.0

    def extract_price(self, product_data):
        try:
            price_dimensions = product_data["pricing"]["terms"]["OnDemand"]
            for key, value in price_dimensions.items():
                return float(value["priceDimensions"][key]["pricePerUnit"]["USD"])
        except KeyError:
            try:
                price_dimensions = product_data["terms"]["OnDemand"]
                for key, value in price_dimensions.items():
                    for k, v in value["priceDimensions"].items():
                        if v["pricePerUnit"] and "USD" in v["pricePerUnit"]:
                            return float(v["pricePerUnit"]["USD"])
            except KeyError as e:
                print(f"Key error: {e} in product_data: {product_data}")
            except ValueError as e:
                print(f"Value error: {e} in product_data: {product_data}")
        return 0.0
