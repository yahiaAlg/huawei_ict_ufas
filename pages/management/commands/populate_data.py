from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import os
from datetime import datetime
from pages.models import Announcement, Course


class Command(BaseCommand):
    help = "Populates the database with initial announcements and courses"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to populate database...")

        # Create announcements
        self.create_announcements()

        # Create courses
        self.create_courses()

        self.stdout.write(self.style.SUCCESS("Successfully populated database!"))

    def create_announcements(self):
        # Delete existing announcements
        Announcement.objects.all().delete()
        self.stdout.write("Deleted existing announcements")

        # Create announcements
        announcements = [
            {
                "title": "Opening of the Huawei ICT Academy at Sétif 1 University, Ferhat ABBAS: UFAS1 Huawei ICT Academy",
                "description": "Official opening ceremony of the Huawei ICT Academy at Sétif 1 University.",
                "date": datetime(2017, 12, 17, 9, 30),
                "location": "Auditorium Mouloud Kacem Naït Belkacem",
                "image_path": "images/Hero-Banner-UFAS(1).png",
                "is_rtl": False,
            },
            {
                "title": "افتتاح أكاديمية هواوي لتكنولوجيا المعلومات والاتصالات في جامعة سطيف 1، فرحات عباس: أكاديمية هواوي لتكنولوجيا المعلومات والاتصالات UFAS1",
                "description": "حفل الافتتاح الرسمي لأكاديمية هواوي لتكنولوجيا المعلومات والاتصالات في جامعة سطيف 1.",
                "date": datetime(2017, 12, 17, 9, 30),
                "location": "قاعة مولود قاسم نايت بلقاسم",
                "image_path": "images/Hero-Banner-UFAS(1).png",
                "is_rtl": True,
            },
        ]

        for idx, announcement_data in enumerate(announcements):
            image_path = announcement_data.pop("image_path")

            # Get image from static files
            try:
                # Check if static file exists
                static_path = os.path.join("pages/static", image_path)
                if os.path.exists(static_path):
                    with open(static_path, "rb") as f:
                        image_content = f.read()
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Image not found: {static_path}")
                    )
                    continue

                # Create image file in media
                file_name = os.path.basename(image_path)
                media_path = f"images/{file_name}"

                # Create announcement
                announcement = Announcement(**announcement_data)
                announcement.image.save(
                    file_name, ContentFile(image_content), save=False
                )
                announcement.save()

                self.stdout.write(f"Created announcement: {announcement.title[:30]}...")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating announcement {idx+1}: {str(e)}")
                )

    def create_courses(self):
        # Delete existing courses
        Course.objects.all().delete()
        self.stdout.write("Deleted existing courses")

        # Create courses
        courses = [
            {
                "name": "DataCom",
                "description": "Master data communication networks and infrastructure",
                "image_path": "images/datacom.webp",
                "slug": "datacom",
            },
            {
                "name": "AI",
                "description": "Explore artificial intelligence and machine learning",
                "image_path": "images/ai.jpg",
                "slug": "ai",
            },
            {
                "name": "Big Data",
                "description": "Learn big data analytics and processing",
                "image_path": "images/big-data.jpg",
                "slug": "big-data",
            },
            {
                "name": "Cloud",
                "description": "Master cloud computing and services",
                "image_path": "images/cloud.jpg",
                "slug": "cloud",
            },
            {
                "name": "IoT",
                "description": "Internet of Things development and applications",
                "image_path": "images/iot.webp",
                "slug": "iot",
            },
            {
                "name": "WLAN",
                "description": "Wireless networking and infrastructure",
                "image_path": "images/wlan.webp",
                "slug": "wlan",
            },
        ]

        for idx, course_data in enumerate(courses):
            image_path = course_data.pop("image_path")

            # Get image from static files
            try:
                # Check if static file exists
                static_path = os.path.join("pages/static", image_path)
                if os.path.exists(static_path):
                    with open(static_path, "rb") as f:
                        image_content = f.read()
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Image not found: {static_path}")
                    )
                    continue

                # Create image file in media
                file_name = os.path.basename(image_path)
                media_path = f"images/{file_name}"

                # Create course
                course = Course(**course_data)
                course.image.save(file_name, ContentFile(image_content), save=False)
                course.save()

                self.stdout.write(f"Created course: {course.name}")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating course {idx+1}: {str(e)}")
                )
