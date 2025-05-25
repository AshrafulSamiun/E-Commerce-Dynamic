from django.db import models

from django.db.models import Avg, Count
from django.utils.text import slugify
from accounts.models import CustomUser

# Create your models here.
class TimeStampModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    inserted_by = models.IntegerField( blank=True, null=True)
    updated_by = models.IntegerField( blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Product(TimeStampModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    specification = models.TextField()
    slug = models.SlugField(max_length=200, unique=True,blank=True)  # Unique slug for the product
    sku = models.CharField(max_length=100, null=True,blank=True) # Stock Keeping Unit
    weight = models.DecimalField(max_digits=10, decimal_places=2)   
    dimensions = models.CharField(max_length=100 , null=True,blank=True)  # e.g., "10x20x30 cm"
    price = models.DecimalField(max_digits=10, decimal_places=2 , null=True,blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Discount percentage
    stock = models.PositiveIntegerField(default=0)  # Number of items in stock
    available = models.BooleanField(default=True)
    brand=models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, related_name='products') 
    currency=models.ForeignKey('Currency', on_delete=models.SET_NULL, null=True, related_name='products')
    rating = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.price}"
        

class Category(TimeStampModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True,blank=True)  # Unique slug for the category
    category_image = models.ImageField(upload_to="categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
   
class Brand(TimeStampModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True,blank=True)  # Unique slug for the brand    


    def __str__(self):
        return f"{self.name}"
    

class Currency(TimeStampModel):
    code=models.CharField(max_length=10)  # e.g., "USD", "EUR"
    symbol=models.CharField(max_length=10)  # e.g., "$", "€"
    name=models.CharField(max_length=100)  # e.g., "US Dollar", "Euro"
    exchange_rate=models.DecimalField(max_digits=10, decimal_places=4)  # Exchange rate against a base currency (e.g., USD)
    is_default=models.BooleanField(default=False)  # True if this is the base currency

    def __str__(self):
        return f"{self.name} ({self.code})"

class Color(TimeStampModel):
    name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7)  # e.g., "#FFFFFF" for white

    def __str__(self):
        return f"{self.name} ({self.hex_code})"
    

class Size(TimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} -{self.name}"

class ColorSize(TimeStampModel):
    color = models.ForeignKey(Color,on_delete=models.SET_NULL, null=True, related_name='color_sizes')
    size = models.ForeignKey(Size,on_delete=models.SET_NULL, null=True, related_name='color_sizes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='color_sizes')
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price for this specific color and size combination
    stock = models.PositiveIntegerField(default=0)  # Stock for this specific color and size combination
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Discount percentage for this specific color and size combination

    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size.name}"

class ProductImage(TimeStampModel):
    product = models.ForeignKey(Product,  on_delete=models.CASCADE, related_name='images')
    image_path = models.ImageField(upload_to='products/images')  
    is_primary = models.BooleanField(default=False)  # True if this is the primary image for the product
    color_size = models.ForeignKey(ColorSize, on_delete=models.SET_NULL, null=True)  # Color and size

    def __str__(self):
        return f"{self.product.name} - {self.color_size}"  


class ProductCategory(TimeStampModel):
    product = models.ForeignKey(Product,  on_delete=models.SET_NULL, null=True, related_name='product_categories')
    category = models.ForeignKey(Category,  on_delete=models.SET_NULL, null=True, related_name='product_categories')
    is_primary = models.BooleanField(default=False)  # True if this is the primary category for the product

    def __str__(self):
        return f"{self.product.name} - {self.category.name}"
    

class ProductReview(TimeStampModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    rating = models.DecimalField(max_digits=5, decimal_places=2,default=0.00, null=True, blank=True)
    review = models.TextField(max_length=500, blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    
    def __str__(self):
        return f"Review by {self.user.full_name} for {self.product.name}"