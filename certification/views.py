from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Certification
from .serializers import CertificationSerializer
from utils import get_object_or_404_custom, not_found_response


class CertificationListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all certifications",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('course_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter certifications mapped to a course"),
        ],
        responses={200: CertificationSerializer(many=True)}
    )
    def get(self, request):
        qs = Certification.objects.all()
        is_active = request.query_params.get('is_active')
        name = request.query_params.get('name')
        course_id = request.query_params.get('course_id')

        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        if name:
            qs = qs.filter(name__icontains=name)
        if course_id:
            qs = qs.filter(coursecertificationmapping__course_id=course_id, coursecertificationmapping__is_active=True)

        serializer = CertificationSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a certification",
        request_body=CertificationSerializer,
        responses={201: CertificationSerializer, 400: "Validation error"}
    )
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificationDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a certification", responses={200: CertificationSerializer, 404: "Not found"})
    def get(self, request, pk):
        cert = get_object_or_404_custom(Certification, pk=pk)
        if cert is None:
            return not_found_response('Certification')
        return Response(CertificationSerializer(cert).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update a certification (full)", request_body=CertificationSerializer, responses={200: CertificationSerializer, 404: "Not found"})
    def put(self, request, pk):
        cert = get_object_or_404_custom(Certification, pk=pk)
        if cert is None:
            return not_found_response('Certification')
        serializer = CertificationSerializer(cert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Partial update a certification", request_body=CertificationSerializer, responses={200: CertificationSerializer, 404: "Not found"})
    def patch(self, request, pk):
        cert = get_object_or_404_custom(Certification, pk=pk)
        if cert is None:
            return not_found_response('Certification')
        serializer = CertificationSerializer(cert, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Soft delete a certification", responses={200: "Deactivated", 404: "Not found"})
    def delete(self, request, pk):
        cert = get_object_or_404_custom(Certification, pk=pk)
        if cert is None:
            return not_found_response('Certification')
        cert.is_active = False
        cert.save()
        return Response({'message': 'Certification deactivated successfully.'}, status=status.HTTP_200_OK)
