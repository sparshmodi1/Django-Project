from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Vendor
from .serializers import VendorSerializer
from utils import get_object_or_404_custom, not_found_response


class VendorListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all vendors",
        operation_description="Returns a list of all vendors. Filter by is_active using query param.",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description="Filter by active status"),
            openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Filter by name (partial match)"),
        ],
        responses={200: VendorSerializer(many=True)}
    )
    def get(self, request):
        qs = Vendor.objects.all()
        is_active = request.query_params.get('is_active')
        name = request.query_params.get('name')
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        if name:
            qs = qs.filter(name__icontains=name)
        serializer = VendorSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a vendor",
        request_body=VendorSerializer,
        responses={201: VendorSerializer, 400: "Validation error"}
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailView(APIView):

    @swagger_auto_schema(
        operation_summary="Retrieve a vendor",
        responses={200: VendorSerializer, 404: "Not found"}
    )
    def get(self, request, pk):
        vendor = get_object_or_404_custom(Vendor, pk=pk)
        if vendor is None:
            return not_found_response('Vendor')
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a vendor (full)",
        request_body=VendorSerializer,
        responses={200: VendorSerializer, 400: "Validation error", 404: "Not found"}
    )
    def put(self, request, pk):
        vendor = get_object_or_404_custom(Vendor, pk=pk)
        if vendor is None:
            return not_found_response('Vendor')
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partial update a vendor",
        request_body=VendorSerializer,
        responses={200: VendorSerializer, 400: "Validation error", 404: "Not found"}
    )
    def patch(self, request, pk):
        vendor = get_object_or_404_custom(Vendor, pk=pk)
        if vendor is None:
            return not_found_response('Vendor')
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Soft delete a vendor",
        responses={200: "Vendor deactivated", 404: "Not found"}
    )
    def delete(self, request, pk):
        vendor = get_object_or_404_custom(Vendor, pk=pk)
        if vendor is None:
            return not_found_response('Vendor')
        vendor.is_active = False
        vendor.save()
        return Response({'message': 'Vendor deactivated successfully.'}, status=status.HTTP_200_OK)
