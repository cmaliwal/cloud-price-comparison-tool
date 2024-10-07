from abc import ABC, abstractmethod

class CloudProvider(ABC):
    @abstractmethod
    def get_prices(self, region, service_code):
        pass

    @abstractmethod
    def parse_data(self, response):
        pass
