from django.db import models
from utils import TimeStampedModel
from product.models import Product
from course.models import Course


class ProductCourseMapping(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productcoursemapping')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='productcoursemapping')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_course_mapping'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['product', 'course'], name='unique_product_course')
        ]

    def __str__(self):
        return f"{self.product.name} → {self.course.name}"
