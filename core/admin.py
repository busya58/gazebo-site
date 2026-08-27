from django.contrib import admin

from .models import (
    Application,
    Category,
    GalleryImage,
    Product,
    ProductImage,
    ProductVariant,
    Project,
    Review,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "kind",
        "is_active",
        "sort_order",
    )
    list_filter = ("kind", "is_active")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "kind",
        "category",
        "price",
        "is_available",
        "is_popular",
        "is_new",
        "views_count",
    )
    list_filter = (
        "kind",
        "season",
        "is_available",
        "is_popular",
        "is_new",
    )
    list_editable = (
        "price",
        "is_available",
        "is_popular",
        "is_new",
    )
    search_fields = (
        "title",
        "article",
        "short_description",
    )
    readonly_fields = (
        "views_count",
        "created_at",
        "updated_at",
    )
    inlines = (
        ProductVariantInline,
        ProductImageInline,
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project_type",
        "approximate_price",
        "is_published",
        "sort_order",
    )
    list_filter = (
        "project_type",
        "is_published",
    )
    list_editable = (
        "is_published",
        "sort_order",
    )
    search_fields = (
        "title",
        "description",
        "installation_location",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "rating",
        "product",
        "is_published",
        "created_at",
    )
    list_filter = (
        "rating",
        "is_published",
    )
    list_editable = ("is_published",)
    search_fields = ("name", "text")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_published",
        "sort_order",
    )
    list_editable = (
        "is_published",
        "sort_order",
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "project_type",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "project_type",
        "created_at",
    )
    list_editable = ("status",)
    search_fields = (
        "name",
        "phone",
        "email",
        "selected_model",
        "address",
    )
    readonly_fields = ("created_at",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "is_main",
        "sort_order",
    )
    list_filter = ("is_main",)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "dimensions",
        "price",
        "is_default",
        "sort_order",
    )
    list_filter = ("is_default",)