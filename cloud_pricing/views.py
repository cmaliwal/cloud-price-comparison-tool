from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import CloudInstancePrice
from .serializers import CloudInstancePriceSerializer


class CloudInstancePriceList(ListAPIView):
    serializer_class = CloudInstancePriceSerializer

    def get_queryset(self):
        cloud_type = self.request.GET.get("cloud_type", None)
        location = self.request.GET.get("location", None)
        min_vcpu = self.request.GET.get("min_vcpu", None)
        max_vcpu = self.request.GET.get("max_vcpu", None)
        min_ram_gb = self.request.GET.get("min_ram_gb", None)
        max_ram_gb = self.request.GET.get("max_ram_gb", None)

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

        queryset = (
            queryset.values("vcpu", "ram_gb")
            .annotate(instance_count=Count("id"))
            .order_by("vcpu", "ram_gb")
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        collection_data = []
        for group in queryset:
            vcpu = group["vcpu"]
            ram_gb = group["ram_gb"]
            instance_count = group["instance_count"]
            instances = CloudInstancePrice.objects.filter(
                vcpu=vcpu, ram_gb=ram_gb
            )

            serializer = self.get_serializer(instances, many=True)

            collection_data.append(
                {
                    "vcpu": vcpu,
                    "ram_gb": ram_gb,
                    "instance_count": instance_count,
                    "instances": serializer.data,
                }
            )

        return Response(collection_data)
