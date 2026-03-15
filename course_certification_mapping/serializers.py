from rest_framework import serializers
from .models import CourseCertificationMapping
from course.models import Course
from certification.models import Certification


class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    certification_name = serializers.CharField(source='certification.name', read_only=True)

    class Meta:
        model = CourseCertificationMapping
        fields = [
            'id', 'course', 'course_name', 'certification', 'certification_name',
            'primary_mapping', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'course_name', 'certification_name', 'created_at', 'updated_at']

    def validate_course(self, value):
        if not Course.objects.filter(pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError("Course does not exist or is inactive.")
        return value

    def validate_certification(self, value):
        if not Certification.objects.filter(pk=value.pk, is_active=True).exists():
            raise serializers.ValidationError("Certification does not exist or is inactive.")
        return value

    def validate(self, attrs):
        course = attrs.get('course', getattr(self.instance, 'course', None))
        certification = attrs.get('certification', getattr(self.instance, 'certification', None))
        primary_mapping = attrs.get('primary_mapping', getattr(self.instance, 'primary_mapping', False))

        # Duplicate mapping check
        qs = CourseCertificationMapping.objects.filter(course=course, certification=certification)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This course-certification mapping already exists.")

        # Single primary mapping per course
        if primary_mapping:
            primary_qs = CourseCertificationMapping.objects.filter(course=course, primary_mapping=True)
            if self.instance:
                primary_qs = primary_qs.exclude(pk=self.instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This course already has a primary certification mapping. Only one primary mapping is allowed per course."
                )

        return attrs
