from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from utils.models import BaseModel
from users.models import User


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")

    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pincode = models.IntegerField(
        validators=[MaxValueValidator(999999), MinValueValidator(100000)]
    )
    contact_number = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.full_name + " - " + self.address


class Category(BaseModel):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    price = models.PositiveIntegerField()

    image = models.ImageField(upload_to="product/")

    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(0)], null=True, blank=True
    )

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    def __str__(self) -> str:
        return self.title


class ProductAmount(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_amounts"
    )

    amount = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(blank=True)

    def __str__(self) -> str:
        return f"{self.product_id} - {self.amount}"

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.amount
        super().save(*args, **kwargs)


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(through=ProductAmount)

    promotional_discount = models.PositiveIntegerField(default=0)
    shipping_fee = models.PositiveIntegerField(default=0)

    total_price = models.PositiveBigIntegerField()

    is_paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user_id} - {self.total_price}"
