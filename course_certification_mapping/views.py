from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer
from utils import get_object_or_404_custom, not_found_response


class CourseCertificationMappingListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all course-certification mappings",
        manual_parameters=[
            openapi.Parameter('course_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter by course"),
            openapi.Parameter('certification_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter by certification"),
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('primary_mapping', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: CourseCertificationMappingSerializer(many=True)}
    )
    def get(self, request):
        qs = CourseCertificationMapping.objects.select_related('course', 'certification').all()
        course_id = request.query_params.get('course_id')
        certification_id = request.query_params.get('certification_id')
        is_active = request.query_params.get('is_active')
        primary_mapping = request.query_params.get('primary_mapping')

        if course_id:
            qs = qs.filter(course_id=course_id)
        if certification_id:
            qs = qs.filter(certification_id=certification_id)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        if primary_mapping is not None:
            qs = qs.filter(primary_mapping=primary_mapping.lower() == 'true')

        serializer = CourseCertificationMappingSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={201: CourseCertificationMappingSerializer, 400: "Validation error"}
    )
    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCertificationMappingDetailView(APIView):

    @swagger_auto_schema(
        operation_summary="Retrieve a course-certification mapping",
        responses={200: CourseCertificationMappingSerializer, 404: "Not found"}
    )
    def get(self, request, pk):
        mapping = get_object_or_404_custom(CourseCertificationMapping, pk=pk)
        if mapping is None:
            return not_found_response('CourseCertificationMapping')
        return Response(CourseCertificationMappingSerializer(mapping).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a course-certification mapping (full)",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer, 400: "Validation error", 404: "Not found"}
    )
    def put(self, request, pk):
        mapping = get_object_or_404_custom(CourseCertificationMapping, pk=pk)
        if mapping is None:
            return not_found_response('CourseCertificationMapping')
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partial update a course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer, 404: "Not found"}
    )
    def patch(self, request, pk):
        mapping = get_object_or_404_custom(CourseCertificationMapping, pk=pk)
        if mapping is None:
            return not_found_response('CourseCertificationMapping')
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Soft delete a course-certification mapping",
        responses={200: "Deactivated", 404: "Not found"}
    )
    def delete(self, request, pk):
        mapping = get_object_or_404_custom(CourseCertificationMapping, pk=pk)
        if mapping is None:
            return not_found_response('CourseCertificationMapping')
        mapping.is_active = False
        mapping.save()
        return Response({'message': 'CourseCertificationMapping deactivated successfully.'}, status=status.HTTP_200_OK)
