from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Course
from .serializers import CourseSerializer
from utils import get_object_or_404_custom, not_found_response


class CourseListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all courses",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('product_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter courses mapped to a product"),
        ],
        responses={200: CourseSerializer(many=True)}
    )
    def get(self, request):
        qs = Course.objects.all()
        is_active = request.query_params.get('is_active')
        name = request.query_params.get('name')
        product_id = request.query_params.get('product_id')

        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        if name:
            qs = qs.filter(name__icontains=name)
        if product_id:
            qs = qs.filter(productcoursemapping__product_id=product_id, productcoursemapping__is_active=True)

        serializer = CourseSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a course",
        request_body=CourseSerializer,
        responses={201: CourseSerializer, 400: "Validation error"}
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a course", responses={200: CourseSerializer, 404: "Not found"})
    def get(self, request, pk):
        course = get_object_or_404_custom(Course, pk=pk)
        if course is None:
            return not_found_response('Course')
        return Response(CourseSerializer(course).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update a course (full)", request_body=CourseSerializer, responses={200: CourseSerializer, 400: "Validation error", 404: "Not found"})
    def put(self, request, pk):
        course = get_object_or_404_custom(Course, pk=pk)
        if course is None:
            return not_found_response('Course')
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Partial update a course", request_body=CourseSerializer, responses={200: CourseSerializer, 404: "Not found"})
    def patch(self, request, pk):
        course = get_object_or_404_custom(Course, pk=pk)
        if course is None:
            return not_found_response('Course')
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Soft delete a course", responses={200: "Deactivated", 404: "Not found"})
    def delete(self, request, pk):
        course = get_object_or_404_custom(Course, pk=pk)
        if course is None:
            return not_found_response('Course')
        course.is_active = False
        course.save()
        return Response({'message': 'Course deactivated successfully.'}, status=status.HTTP_200_OK)
