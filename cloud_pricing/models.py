from django.db import models


class CloudInstancePrice(models.Model):
    cloud_type = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    instance_type = models.CharField(max_length=50)
    instance_family = models.CharField(max_length=50)
    vcpu = models.IntegerField()
    ram_gb = models.FloatField()
    price_per_hour = models.FloatField()
    effective_date = models.DateField()

    class Meta:
        verbose_name = "Cloud Instance Price"
        verbose_name_plural = "Cloud Instance Prices"
        ordering = ["effective_date"]

    def __str__(self):
        return (
            f"{self.instance_type} ({self.cloud_type}) - {self.effective_date}"
        )
