from django.contrib import admin

from .models import Application
from .models import Review

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "project_type",
        "phone",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "project_type",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "rating",
        "is_published",
        "created_at",
    )

    list_filter = (
        "is_published",
        "rating",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "text",
    )

    list_editable = (
        "is_published",
    )

    readonly_fields = (
        "user",
        "created_at",
    )    