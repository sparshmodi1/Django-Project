from django.db import models
from utils import TimeStampedModel
from vendor.models import Vendor
from product.models import Product


class VendorProductMapping(TimeStampedModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendorproductmapping')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='vendorproductmapping')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'vendor_product_mapping'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['vendor', 'product'], name='unique_vendor_product')
        ]

    def __str__(self):
        return f"{self.vendor.name} → {self.product.name}"
