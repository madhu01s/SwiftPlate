from django.urls import path
from . import views


app_name = 'orders'


urlpatterns = [

    # =========================
    # AUTHENTICATION
    # =========================

    path(
        'signup/',
        views.signup,
        name='signup'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),


    # =========================
    # HOME PAGE
    # =========================

    path(
        '',
        views.home,
        name='home'
    ),


    # =========================
    # CART
    # =========================

    path(
        'cart/',
        views.view_cart,
        name='view_cart'
    ),

    path(
        'add-to-cart/<int:food_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'update-cart/<int:cart_id>/',
        views.update_cart_quantity,
        name='update_cart_quantity'
    ),

    path(
        'delete-cart-item/<int:cart_id>/',
        views.delete_cart_item,
        name='delete_cart_item'
    ),


    # =========================
    # ADDRESS
    # =========================

    path(
        'address/',
        views.address,
        name='address'
    ),

    path(
        'delete-address/<int:address_id>/',
        views.delete_address,
        name='delete_address'
    ),


    # =========================
    # ORDER
    # =========================

    path(
        'confirm-order/',
        views.confirm_order,
        name='confirm_order'
    ),

    path(
        'place-order/',
        views.place_order,
        name='place_order'
    ),

    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),

    path(
        'delete-order/<int:order_id>/',
        views.delete_order,
        name='delete_order'
    ),


    # =========================
    # PAYMENT
    # =========================

    path(
        'create-checkout-session/',
        views.create_stripe_session,
        name='create_stripe_session'
    ),

    path(
        'payment-success/<int:order_id>/',
        views.payment_success,
        name='payment_success'
    ),

]