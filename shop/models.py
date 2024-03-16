from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from utils.models import BaseModel
from users.models import User


class Status(models.TextChoices):
    ONGOING = "Ongoing"
    DELIVERED = "Delivered"
    UPCOMMING = "Upcomming"


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

    category = models.ManyToManyField(Category, related_name="products")

    def __str__(self) -> str:
        return self.title


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="carts")

    amount = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(blank=True)

    def __str__(self) -> str:
        return f"{self.product_id} - {self.amount}"

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.amount
        super().save(*args, **kwargs)


class Checkout(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checkouts")
    carts = models.ManyToManyField(Cart, related_name="checkouts")

    promotional_discount = models.PositiveIntegerField(default=0)
    shipping_fee = models.PositiveIntegerField(default=0)

    total_price = models.PositiveBigIntegerField(blank=True)

    is_paid = models.BooleanField(default=False)

    status = models.CharField(
        max_length=64,
        choices=Status.choices,
        default=Status.ONGOING,
    )

    def __str__(self) -> str:
        return f"{self.user_id} - {self.total_price}"

    # def save(self, *args, **kwargs):
    #     print(f"\n\n{self.carts.aaggregate(models.Sum('price'))}\n\n")
    #     self.total_price = (
    #         self.promotional_discount
    #         + self.shipping_fee
    #         + self.carts.all().annotate(prices_sum=models.SUM("price"))["prices_sum"]
    #     )
    #     super().save(*args, **kwargs)
