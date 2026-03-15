from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer
from utils import get_object_or_404_custom, not_found_response


class VendorProductMappingListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all vendor-product mappings",
        manual_parameters=[
            openapi.Parameter('vendor_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter by vendor"),
            openapi.Parameter('product_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter by product"),
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('primary_mapping', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: VendorProductMappingSerializer(many=True)}
    )
    def get(self, request):
        qs = VendorProductMapping.objects.select_related('vendor', 'product').all()
        vendor_id = request.query_params.get('vendor_id')
        product_id = request.query_params.get('product_id')
        is_active = request.query_params.get('is_active')
        primary_mapping = request.query_params.get('primary_mapping')

        if vendor_id:
            qs = qs.filter(vendor_id=vendor_id)
        if product_id:
            qs = qs.filter(product_id=product_id)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        if primary_mapping is not None:
            qs = qs.filter(primary_mapping=primary_mapping.lower() == 'true')

        serializer = VendorProductMappingSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a vendor-product mapping",
        request_body=VendorProductMappingSerializer,
        responses={201: VendorProductMappingSerializer, 400: "Validation error"}
    )
    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductMappingDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a vendor-product mapping", responses={200: VendorProductMappingSerializer, 404: "Not found"})
    def get(self, request, pk):
        mapping = get_object_or_404_custom(VendorProductMapping, pk=pk)
        if mapping is None:
            return not_found_response('VendorProductMapping')
        return Response(VendorProductMappingSerializer(mapping).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update a vendor-product mapping (full)", request_body=VendorProductMappingSerializer, responses={200: VendorProductMappingSerializer, 400: "Validation error", 404: "Not found"})
    def put(self, request, pk):
        mapping = get_object_or_404_custom(VendorProductMapping, pk=pk)
        if mapping is None:
            return not_found_response('VendorProductMapping')
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Partial update a vendor-product mapping", request_body=VendorProductMappingSerializer, responses={200: VendorProductMappingSerializer, 404: "Not found"})
    def patch(self, request, pk):
        mapping = get_object_or_404_custom(VendorProductMapping, pk=pk)
        if mapping is None:
            return not_found_response('VendorProductMapping')
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Soft delete a vendor-product mapping", responses={200: "Deactivated", 404: "Not found"})
    def delete(self, request, pk):
        mapping = get_object_or_404_custom(VendorProductMapping, pk=pk)
        if mapping is None:
            return not_found_response('VendorProductMapping')
        mapping.is_active = False
        mapping.save()
        return Response({'message': 'VendorProductMapping deactivated successfully.'}, status=status.HTTP_200_OK)
