from rest_framework import serializers
from .models import VendorProductMapping
from vendor.models import Vendor
from product.models import Product


class VendorProductMappingSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = VendorProductMapping
        fields = [
            'id', 'vendor', 'vendor_name', 'product', 'product_name',
            'primary_mapping', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'vendor_name', 'product_name', 'created_at', 'updated_at']

    def validate_vendor(self, value):
        if not Vendor.objects.filter(pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError("Vendor does not exist or is inactive.")
        return value

    def validate_product(self, value):
        if not Product.objects.filter(pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError("Product does not exist or is inactive.")
        return value

    def validate(self, attrs):
        vendor = attrs.get('vendor', getattr(self.instance, 'vendor', None))
        product = attrs.get('product', getattr(self.instance, 'product', None))
        primary_mapping = attrs.get('primary_mapping', getattr(self.instance, 'primary_mapping', False))

        # Duplicate mapping check
        qs = VendorProductMapping.objects.filter(vendor=vendor, product=product)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This vendor-product mapping already exists.")

        # Single primary mapping per vendor
        if primary_mapping:
            primary_qs = VendorProductMapping.objects.filter(vendor=vendor, primary_mapping=True)
            if self.instance:
                primary_qs = primary_qs.exclude(pk=self.instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This vendor already has a primary product mapping. Only one primary mapping is allowed per vendor."
                )

        return attrs
