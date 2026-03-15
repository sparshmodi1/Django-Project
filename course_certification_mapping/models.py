from django.db import models
from utils import TimeStampedModel
from course.models import Course
from certification.models import Certification


class CourseCertificationMapping(TimeStampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='coursecertificationmapping')
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name='coursecertificationmapping')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'course_certification_mapping'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['course', 'certification'], name='unique_course_certification')
        ]

    def __str__(self):
        return f"{self.course.name} → {self.certification.name}"
