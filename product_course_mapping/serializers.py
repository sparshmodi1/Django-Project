from rest_framework import serializers
from .models import ProductCourseMapping
from product.models import Product
from course.models import Course


class ProductCourseMappingSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = ProductCourseMapping
        fields = [
            'id', 'product', 'product_name', 'course', 'course_name',
            'primary_mapping', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'product_name', 'course_name', 'created_at', 'updated_at']

    def validate_product(self, value):
        if not Product.objects.filter(pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError("Product does not exist or is inactive.")
        return value

    def validate_course(self, value):
        if not Course.objects.filter(pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError("Course does not exist or is inactive.")
        return value

    def validate(self, attrs):
        product = attrs.get('product', getattr(self.instance, 'product', None))
        course = attrs.get('course', getattr(self.instance, 'course', None))
        primary_mapping = attrs.get('primary_mapping', getattr(self.instance, 'primary_mapping', False))

        # Duplicate mapping check
        qs = ProductCourseMapping.objects.filter(product=product, course=course)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This product-course mapping already exists.")

        # Single primary mapping per product
        if primary_mapping:
            primary_qs = ProductCourseMapping.objects.filter(product=product, primary_mapping=True)
            if self.instance:
                primary_qs = primary_qs.exclude(pk=self.instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This product already has a primary course mapping. Only one primary mapping is allowed per product."
                )

        return attrs
