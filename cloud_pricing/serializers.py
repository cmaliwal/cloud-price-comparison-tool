from rest_framework import serializers

from .models import CloudInstancePrice


class CloudInstancePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudInstancePrice
        fields = "__all__"
