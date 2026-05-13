from django.db import models
from django.contrib.auth.models import User


# =========================
# CATEGORY MODEL
# =========================

class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    image = models.ImageField(
        upload_to='category_images/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# =========================
# FOOD ITEM MODEL
# =========================

class FoodItem(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='foods'
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='food_images/'
    )

    is_available = models.BooleanField(default=True)

    is_veg = models.BooleanField(default=False)

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=4.5
    )

    preparation_time = models.PositiveIntegerField(
        default=20,
        help_text="Time in minutes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-id']),
            models.Index(fields=['is_available', '-id']),
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.name


# =========================
# CART MODEL
# =========================

class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'food_item']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['user', '-created_at']),
        ]

    @property
    def total_price(self):
        return self.food_item.price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.food_item.name}"


# =========================
# ORDER MODEL
# =========================

class Order(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    PAYMENT_CHOICES = (
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Online Payment', 'Online Payment'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    address = models.JSONField(
        blank=True,
        null=True
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    delivery_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=40
    )

    gst_amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_CHOICES,
        default='Cash on Delivery'
    )

    payment_status = models.BooleanField(default=False)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


# =========================
# ORDER ITEM MODEL
# =========================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )

    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"


# =========================
# USER ADDRESS MODEL
# =========================

class UserAddress(models.Model):

    ADDRESS_TYPES = (
        ('Home', 'Home'),
        ('Work', 'Work'),
        ('Other', 'Other'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPES,
        default='Home'
    )

    name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    area = models.CharField(max_length=200)

    city = models.CharField(max_length=100)

    landmark = models.CharField(
        max_length=200,
        blank=True
    )

    district = models.CharField(max_length=100)

    zipcode = models.CharField(max_length=20)

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.city}"


# =========================
# FAVORITE MODEL
# =========================

class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'food_item']

    def __str__(self):
        return f"{self.user.username} likes {self.food_item.name}"