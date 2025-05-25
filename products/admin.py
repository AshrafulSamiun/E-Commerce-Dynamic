from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import now
# Register your models here.
from .models import Product, Category, Brand, Currency, Color, ProductImage, ProductCategory, ColorSize, Size, ProductReview


from django.contrib import admin

admin.site.site_header = "Cloud State E-commerce Admin Panel"         # Top-left header
admin.site.site_title = "Cloud State E-commerce Admin"                # Title on browser tab
admin.site.index_title = "Welcome to Cloud State E-commerce Dashboard"  # Title above the app list


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    search_fields = ['name']
    
    def save_model(self, request, obj, form, change):
        if not change:  # This is a new object
            obj.inserted_by = request.user.id
        obj.updated_by = request.user.id
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.is_active = False
        obj.deleted_at = now()
        obj.updated_by = request.user.id
        obj.save()

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    search_fields = ['name']

    
    def save_model(self, request, obj, form, change):
        if not change:  # This is a new object
            obj.inserted_by = request.user.id
        obj.updated_by = request.user.id
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.is_active = False
        obj.deleted_at = now()
        obj.updated_by = request.user.id
        obj.save()


@admin.register(ColorSize)
class ColorSizeAdmin(admin.ModelAdmin):
    search_fields = ['name','color__name','size__name']
    list_display = ('product', 'color', 'size', 'price', 'stock')

    
    def save_model(self, request, obj, form, change):
        if not change:  # This is a new object
            obj.inserted_by = request.user.id
        obj.updated_by = request.user.id
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.is_active = False
        obj.deleted_at = now()
        obj.updated_by = request.user.id
        obj.save()

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ['name','description', 'slug']
    list_display = ('name',  'description', 'slug')      

    
    def save_model(self, request, obj, form, change):
        if not change:  # This is a new object
            obj.inserted_by = request.user.id
        obj.updated_by = request.user.id
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.is_active = False
        obj.deleted_at = now()
        obj.updated_by = request.user.id
        obj.save()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name','slug']
    list_display = ('name', 'slug')

    
    def save_model(self, request, obj, form, change):
        if not change:  # This is a new object
            obj.inserted_by = request.user.id
        obj.updated_by = request.user.id
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.is_active = False
        obj.deleted_at = now()
        obj.updated_by = request.user.id
        obj.save()

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    search_fields = ['code','name']
    list_display = ('code', 'symbol', 'name', 'exchange_rate', 'is_default')

    
    def save_model(self, request, obj, form, change):
        if not change:  # This is a new object
            obj.inserted_by = request.user.id
        obj.updated_by = request.user.id
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.is_active = False
        obj.deleted_at = now()
        obj.updated_by = request.user.id
        obj.save()


# Inline for ColorSize
class ColorSizeInline(admin.TabularInline):
    model = ColorSize
    extra = 1
    autocomplete_fields = ['color', 'size']


# @admin.register(ColorSize)
# class ColorSizeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'stock', 'available', 'brand', 'currency')
#     prepopulated_fields = {"slug": ("name",)}
#     search_fields = ['name', 'description']
#     list_filter = ['available', 'brand', 'currency']



# Inline for ProductCategory
class ProductCategoryInline(admin.TabularInline):
    model = ProductCategory
    extra = 1

# Inline for ProductImage
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

    def image_preview(self, obj):
        if obj.image_path:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image_path.url)
        return "No Image"
    readonly_fields = ['image_preview']
    fields=['image_preview', 'image_path']
    verbose_name_plural="Product Images"

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'available', 'brand', 'currency')
    inlines = [ProductCategoryInline, ProductImageInline,ColorSizeInline]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'description']
    list_filter = ['available', 'brand', 'currency']

    
    def save_model(self, request, obj, form, change):
        if not change:  # This is a new object
            obj.inserted_by = request.user.id
        obj.updated_by = request.user.id
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.is_active = False
        obj.deleted_at = now()
        obj.updated_by = request.user.id
        obj.save()

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview')
    #fields=['product', 'image_path']
    def image_preview(self, obj):
        if obj.image_path:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image_path.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'
    readonly_fields = ['image_preview']

    
    def save_model(self, request, obj, form, change):
        if not change:  # This is a new object
            obj.inserted_by = request.user.id
        obj.updated_by = request.user.id
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.is_active = False
        obj.deleted_at = now()
        obj.updated_by = request.user.id
        obj.save()

admin.site.register([

   
    ProductReview,
    ProductCategory,
    
    

])