from django.contrib import admin
from django.utils import timezone
from .models import Announcement, GalleryImage, Course, Contact


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location", "is_rtl")
    list_filter = ("date", "is_rtl")
    search_fields = ("title", "description", "location")
    date_hierarchy = "date"
    ordering = ("-date",)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "description")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_resolved", "resolved_by")
    list_filter = ("is_resolved", "created_at", "resolved_at")
    search_fields = ("name", "email", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    actions = ["mark_as_resolved"]

    def mark_as_resolved(self, request, queryset):
        for contact in queryset:
            if not contact.is_resolved:
                contact.is_resolved = True
                contact.resolved_by = request.user
                contact.resolved_at = timezone.now()
                contact.save()

        count = queryset.count()
        self.message_user(request, f"{count} contact(s) have been marked as resolved.")

    mark_as_resolved.short_description = "Mark selected contacts as resolved"
