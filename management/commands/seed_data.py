from django.core.management.base import BaseCommand
from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Clear existing
        CourseCertificationMapping.objects.all().delete()
        ProductCourseMapping.objects.all().delete()
        VendorProductMapping.objects.all().delete()
        Certification.objects.all().delete()
        Course.objects.all().delete()
        Product.objects.all().delete()
        Vendor.objects.all().delete()

        # Vendors
        v1 = Vendor.objects.create(name='Tech Corp', code='TECH001', description='Technology vendor')
        v2 = Vendor.objects.create(name='Edu Solutions', code='EDU001', description='Education vendor')
        v3 = Vendor.objects.create(name='Cloud Systems', code='CLOUD001', description='Cloud services vendor')

        # Products
        p1 = Product.objects.create(name='Python Bootcamp', code='PROD001', description='Python programming product')
        p2 = Product.objects.create(name='Data Science Suite', code='PROD002', description='Data science product bundle')
        p3 = Product.objects.create(name='DevOps Package', code='PROD003', description='DevOps tools and training')
        p4 = Product.objects.create(name='Web Development Pro', code='PROD004', description='Full-stack web development')

        # Courses
        c1 = Course.objects.create(name='Python Basics', code='CRS001', description='Introduction to Python')
        c2 = Course.objects.create(name='Python Advanced', code='CRS002', description='Advanced Python programming')
        c3 = Course.objects.create(name='Machine Learning', code='CRS003', description='ML fundamentals')
        c4 = Course.objects.create(name='Docker & Kubernetes', code='CRS004', description='Container orchestration')
        c5 = Course.objects.create(name='React & Node.js', code='CRS005', description='Modern web development')

        # Certifications
        cert1 = Certification.objects.create(name='Python Developer Cert', code='CERT001', description='Certified Python Developer')
        cert2 = Certification.objects.create(name='ML Engineer Cert', code='CERT002', description='Certified ML Engineer')
        cert3 = Certification.objects.create(name='DevOps Professional', code='CERT003', description='Certified DevOps Professional')
        cert4 = Certification.objects.create(name='Full Stack Developer', code='CERT004', description='Certified Full Stack Developer')

        # Vendor → Product mappings
        VendorProductMapping.objects.create(vendor=v1, product=p1, primary_mapping=True)
        VendorProductMapping.objects.create(vendor=v1, product=p3)
        VendorProductMapping.objects.create(vendor=v2, product=p2, primary_mapping=True)
        VendorProductMapping.objects.create(vendor=v2, product=p4)
        VendorProductMapping.objects.create(vendor=v3, product=p3, primary_mapping=True)

        # Product → Course mappings
        ProductCourseMapping.objects.create(product=p1, course=c1, primary_mapping=True)
        ProductCourseMapping.objects.create(product=p1, course=c2)
        ProductCourseMapping.objects.create(product=p2, course=c3, primary_mapping=True)
        ProductCourseMapping.objects.create(product=p3, course=c4, primary_mapping=True)
        ProductCourseMapping.objects.create(product=p4, course=c5, primary_mapping=True)

        # Course → Certification mappings
        CourseCertificationMapping.objects.create(course=c1, certification=cert1, primary_mapping=True)
        CourseCertificationMapping.objects.create(course=c2, certification=cert1)
        CourseCertificationMapping.objects.create(course=c3, certification=cert2, primary_mapping=True)
        CourseCertificationMapping.objects.create(course=c4, certification=cert3, primary_mapping=True)
        CourseCertificationMapping.objects.create(course=c5, certification=cert4, primary_mapping=True)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded: {Vendor.objects.count()} vendors, {Product.objects.count()} products, '
            f'{Course.objects.count()} courses, {Certification.objects.count()} certifications, '
            f'{VendorProductMapping.objects.count()} vendor-product mappings, '
            f'{ProductCourseMapping.objects.count()} product-course mappings, '
            f'{CourseCertificationMapping.objects.count()} course-certification mappings.'
        ))
