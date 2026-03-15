from django.db import models
from rest_framework.response import Response
from rest_framework import status


class TimeStampedModel(models.Model):
    """Abstract base model providing created_at and updated_at fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def get_object_or_404_custom(model, **kwargs):
    """Custom object fetcher that returns None instead of raising Http404."""
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def not_found_response(entity='Object'):
    return Response(
        {'error': f'{entity} not found.'},
        status=status.HTTP_404_NOT_FOUND
    )
