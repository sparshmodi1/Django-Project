from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer
from utils import get_object_or_404_custom, not_found_response


class ProductCourseMappingListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all product-course mappings",
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter by product"),
            openapi.Parameter('course_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter by course"),
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('primary_mapping', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: ProductCourseMappingSerializer(many=True)}
    )
    def get(self, request):
        qs = ProductCourseMapping.objects.select_related('product', 'course').all()
        product_id = request.query_params.get('product_id')
        course_id = request.query_params.get('course_id')
        is_active = request.query_params.get('is_active')
        primary_mapping = request.query_params.get('primary_mapping')

        if product_id:
            qs = qs.filter(product_id=product_id)
        if course_id:
            qs = qs.filter(course_id=course_id)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        if primary_mapping is not None:
            qs = qs.filter(primary_mapping=primary_mapping.lower() == 'true')

        serializer = ProductCourseMappingSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a product-course mapping",
        request_body=ProductCourseMappingSerializer,
        responses={201: ProductCourseMappingSerializer, 400: "Validation error"}
    )
    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a product-course mapping", responses={200: ProductCourseMappingSerializer, 404: "Not found"})
    def get(self, request, pk):
        mapping = get_object_or_404_custom(ProductCourseMapping, pk=pk)
        if mapping is None:
            return not_found_response('ProductCourseMapping')
        return Response(ProductCourseMappingSerializer(mapping).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update a product-course mapping (full)", request_body=ProductCourseMappingSerializer, responses={200: ProductCourseMappingSerializer, 404: "Not found"})
    def put(self, request, pk):
        mapping = get_object_or_404_custom(ProductCourseMapping, pk=pk)
        if mapping is None:
            return not_found_response('ProductCourseMapping')
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Partial update a product-course mapping", request_body=ProductCourseMappingSerializer, responses={200: ProductCourseMappingSerializer, 404: "Not found"})
    def patch(self, request, pk):
        mapping = get_object_or_404_custom(ProductCourseMapping, pk=pk)
        if mapping is None:
            return not_found_response('ProductCourseMapping')
        serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Soft delete a product-course mapping", responses={200: "Deactivated", 404: "Not found"})
    def delete(self, request, pk):
        mapping = get_object_or_404_custom(ProductCourseMapping, pk=pk)
        if mapping is None:
            return not_found_response('ProductCourseMapping')
        mapping.is_active = False
        mapping.save()
        return Response({'message': 'ProductCourseMapping deactivated successfully.'}, status=status.HTTP_200_OK)
