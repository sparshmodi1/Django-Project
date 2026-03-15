from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product
from .serializers import ProductSerializer
from utils import get_object_or_404_custom, not_found_response


class ProductListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all products",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('vendor_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter products mapped to a vendor"),
        ],
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request):
        qs = Product.objects.all()
        is_active = request.query_params.get('is_active')
        name = request.query_params.get('name')
        vendor_id = request.query_params.get('vendor_id')

        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        if name:
            qs = qs.filter(name__icontains=name)
        if vendor_id:
            qs = qs.filter(vendorproductmapping__vendor_id=vendor_id, vendorproductmapping__is_active=True)

        serializer = ProductSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer, 400: "Validation error"}
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a product", responses={200: ProductSerializer, 404: "Not found"})
    def get(self, request, pk):
        product = get_object_or_404_custom(Product, pk=pk)
        if product is None:
            return not_found_response('Product')
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update a product (full)", request_body=ProductSerializer, responses={200: ProductSerializer, 400: "Validation error", 404: "Not found"})
    def put(self, request, pk):
        product = get_object_or_404_custom(Product, pk=pk)
        if product is None:
            return not_found_response('Product')
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Partial update a product", request_body=ProductSerializer, responses={200: ProductSerializer, 400: "Validation error", 404: "Not found"})
    def patch(self, request, pk):
        product = get_object_or_404_custom(Product, pk=pk)
        if product is None:
            return not_found_response('Product')
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Soft delete a product", responses={200: "Deactivated", 404: "Not found"})
    def delete(self, request, pk):
        product = get_object_or_404_custom(Product, pk=pk)
        if product is None:
            return not_found_response('Product')
        product.is_active = False
        product.save()
        return Response({'message': 'Product deactivated successfully.'}, status=status.HTTP_200_OK)
