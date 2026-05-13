from django.contrib import admin
from .models import (
    Category,
    FoodItem,
    Cart,
    Order,
    OrderItem,
    UserAddress,
    Favorite
)


# =========================
# CATEGORY ADMIN
# =========================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'created_at'
    )

    search_fields = (
        'name',
    )

    list_per_page = 10


# =========================
# FOOD ITEM ADMIN
# =========================

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'category',
        'price',
        'rating',
        'is_available',
        'is_veg',
        'created_at'
    )

    list_filter = (
        'category',
        'is_available',
        'is_veg',
    )

    search_fields = (
        'name',
        'description'
    )

    readonly_fields = (
        'created_at',
        'updated_at'
    )

    list_editable = (
        'price',
        'is_available',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 10


# =========================
# CART ADMIN
# =========================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'food_item',
        'quantity',
        'total_price',
        'created_at'
    )

    search_fields = (
        'user__username',
        'food_item__name'
    )

    list_filter = (
        'created_at',
    )

    readonly_fields = (
        'created_at',
        'updated_at'
    )

    list_per_page = 10


# =========================
# ORDER ITEM INLINE
# =========================

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = (
        'food_item',
        'quantity',
        'price',
    )


# =========================
# ORDER ADMIN
# =========================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'total_price',
        'payment_method',
        'payment_status',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'payment_status',
        'payment_method',
    )

    search_fields = (
        'user__username',
    )

    readonly_fields = (
        'created_at',
        'updated_at'
    )

    list_editable = (
        'status',
        'payment_status',
    )

    ordering = (
        '-created_at',
    )

    inlines = [
        OrderItemInline
    ]

    list_per_page = 10


# =========================
# USER ADDRESS ADMIN
# =========================

@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'address_type',
        'city',
        'district',
        'zipcode',
        'is_default'
    )

    search_fields = (
        'user__username',
        'city',
        'district'
    )

    list_filter = (
        'address_type',
        'city',
    )

    list_per_page = 10


# =========================
# FAVORITE ADMIN
# =========================

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'food_item',
        'created_at'
    )

    search_fields = (
        'user__username',
        'food_item__name'
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 10