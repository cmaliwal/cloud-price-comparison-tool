from rest_framework.generics import ListAPIView
from .models import CloudInstancePrice
from .serializers import CloudInstancePriceSerializer

class CloudInstancePriceList(ListAPIView):
    serializer_class = CloudInstancePriceSerializer

    def get_queryset(self):
        cloud_type = self.request.GET.get('cloud_type', None)
        location = self.request.GET.get('location', None)
        min_vcpu = self.request.GET.get('min_vcpu', None)
        max_vcpu = self.request.GET.get('max_vcpu', None)
        min_ram_gb = self.request.GET.get('min_ram_gb', None)
        max_ram_gb = self.request.GET.get('max_ram_gb', None)

        queryset = CloudInstancePrice.objects.all()

        if cloud_type:
            queryset = queryset.filter(cloud_type=cloud_type)

        if location:
            queryset = queryset.filter(location=location)

        if min_vcpu:
            queryset = queryset.filter(vcpu__gte=int(min_vcpu))

        if max_vcpu:
            queryset = queryset.filter(vcpu__lte=int(max_vcpu))

        if min_ram_gb:
            queryset = queryset.filter(ram_gb__gte=float(min_ram_gb))

        if max_ram_gb:
            queryset = queryset.filter(ram_gb__lte=float(max_ram_gb))

        return queryset
