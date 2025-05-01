from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import os
from pages.models import GalleryImage


class Command(BaseCommand):
    help = "Populates the gallery with images from the huawei_setif_event directory"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to populate gallery...")

        # Delete existing gallery images
        GalleryImage.objects.all().delete()
        self.stdout.write("Deleted existing gallery images")

        # Path to the gallery images
        gallery_dir = "media/huawei_setif_event"

        # Make sure the directory exists
        if not os.path.exists(gallery_dir):
            self.stdout.write(self.style.ERROR(f"Directory not found: {gallery_dir}"))
            return

        # Get all image files from the directory
        image_files = [
            f
            for f in os.listdir(gallery_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]

        # Sort files to ensure consistent order
        image_files.sort()

        # Create gallery images
        for i, image_file in enumerate(image_files):
            try:
                file_path = os.path.join(gallery_dir, image_file)

                # Read file content
                with open(file_path, "rb") as f:
                    image_content = f.read()

                # Create gallery image
                title = f"Huawei ICT Academy Event Photo {i+1}"
                description = (
                    f"Photo from the Huawei ICT Academy Event at Sétif 1 University"
                )

                gallery_image = GalleryImage(title=title, description=description)

                # Save image file
                gallery_image.image.save(
                    image_file, ContentFile(image_content), save=False
                )
                gallery_image.save()

                self.stdout.write(f"Created gallery image: {title}")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error creating gallery image {image_file}: {str(e)}"
                    )
                )

        # Print success message with count
        count = GalleryImage.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully populated gallery with {count} images!")
        )
