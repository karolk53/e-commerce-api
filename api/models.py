import os

from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(ProductCategory,on_delete=models.SET_NULL,null=True)
    image = models.ImageField(upload_to="products_images/")
    image_thumbnail = models.ImageField()

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.image:
    #         self.create_thumbnail()

    def image_name(self):
        return os.path.basename(self.image.name)

    def create_thumbnail(self):
        if not self.image_thumbnail:
            image = Image.open(self.image.path)
            image.thumbnail((200, 200))
            thumbnail_path = f'media/products_thumbnails/{self.image_name()}'
            image.save(thumbnail_path)
            self.image_thumbnail = f"products_thumbnails/{self.image_name()}"
            self.save()

    def __str__(self):
        return self.name


@receiver(post_save, sender=Product)
def create_product_thumbnail(sender, instance, created, **kwargs):
    if created and instance.image:
        instance.create_thumbnail()


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class ProductOrder(models.Model):
    client = models.ForeignKey(User,on_delete=models.CASCADE)
    adres = models.TextField(max_length=255)
    products = models.ManyToManyField(OrderItem,related_name='order_items')
    order_date = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField()
    summary_price = models.DecimalField(max_digits=8, decimal_places=2)




