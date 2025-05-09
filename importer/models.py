from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  
    title = models.CharField(max_length=255)
    image_link = models.URLField()
    description = models.TextField()
    link = models.URLField()
    
    price = models.CharField(max_length=50) 
    sale_price = models.CharField(max_length=50, blank=True, null=True)
    shipping = models.CharField(max_length=100, blank=True, null=True) 
    
    item_group_id = models.CharField(max_length=50, blank=True, null=True)
    availability = models.CharField(max_length=50)
    additional_image_links = models.TextField(blank=True, null=True)  
    
    brand = models.CharField(max_length=100)
    gtin = models.BigIntegerField()
    gender = models.CharField(max_length=50, blank=True, null=True)
    google_product_category = models.IntegerField(blank=True, null=True)
    product_type = models.CharField(max_length=100, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    pattern = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    
    product_length = models.CharField(max_length=50, blank=True, null=True)
    product_width = models.CharField(max_length=50, blank=True, null=True)
    product_height = models.CharField(max_length=50, blank=True, null=True)
    product_weight = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    
    lifestyle_image_link = models.URLField(blank=True, null=True)
    max_handling_time = models.IntegerField(blank=True, null=True)
    is_bundle = models.CharField(max_length=10, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    condition = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.title}"




class ImportLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    row_number = models.IntegerField()
    status = models.CharField(max_length=50) 
    message = models.TextField()

class ImportSummary(models.Model):
    file_name = models.CharField(max_length=255)
    total = models.IntegerField()
    success = models.IntegerField()
    warnings = models.IntegerField()
    errors = models.IntegerField()
    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)