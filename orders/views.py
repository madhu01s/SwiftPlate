from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings

from .models import FoodItem, Cart, Order, OrderItem, UserAddress

import stripe
import json


stripe.api_key = settings.STRIPE_SECRET_KEY


# =========================
# SIGNUP
# =========================

def signup(request):
    if request.user.is_authenticated:
        return redirect('orders:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if not username or not email or not password:
            messages.error(request, 'Please fill all fields')
            return redirect('orders:signup')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return redirect('orders:signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('orders:signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('orders:signup')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('orders:login')
    
    return render(request, 'signup.html')


# =========================
# LOGIN
# =========================

def user_login(request):
    if request.user.is_authenticated:
        return redirect('orders:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please fill all fields')
            return redirect('orders:login')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('orders:home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('orders:login')
    
    return render(request, 'login.html')


# =========================
# LOGOUT
# =========================

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('orders:home')


# =========================
# HOME PAGE
# =========================

def home(request):
    # Optimize: use select_related for category if needed
    food_items = FoodItem.objects.filter(
        is_available=True
    ).select_related('category').order_by('-id')

    # Search functionality
    query = request.GET.get('q')

    if query:
        food_items = food_items.filter(name__icontains=query)

    return render(request, 'home.html', {
        'food_items': food_items
    })


# =========================
# ADD TO CART
# =========================

@login_required
@require_POST
def add_to_cart(request, food_id):
    try:
        # Optimize: use select_related if food has foreign keys
        food_item = FoodItem.objects.get(id=food_id)
        
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            food_item=food_item,
            defaults={'quantity': 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save(update_fields=['quantity', 'updated_at'])

        return JsonResponse({
            'success': True,
            'message': 'Item added to cart successfully!',
            'quantity': cart_item.quantity
        })
    except FoodItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Food item not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


# =========================
# VIEW CART
# =========================

@login_required
def view_cart(request):

    cart_items = Cart.objects.filter(
        user=request.user
    ).select_related('food_item', 'food_item__category')

    subtotal = Decimal('0.00')

    for item in cart_items:
        subtotal += item.total_price

    delivery_fee = Decimal('40.00')
    gst = subtotal * Decimal('0.05')

    grand_total = subtotal + delivery_fee + gst

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'gst': gst,
        'grand_total': grand_total
    })


# =========================
# UPDATE CART QUANTITY
# =========================

@login_required
@require_POST
def update_cart_quantity(request, cart_id):

    try:

        data = json.loads(request.body)

        quantity = int(data.get('quantity', 1))

        if quantity < 1:
            return JsonResponse({
                'success': False,
                'message': 'Quantity must be at least 1'
            })

        cart_item = get_object_or_404(
            Cart,
            id=cart_id,
            user=request.user
        )

        cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({
            'success': True,
            'message': 'Quantity updated successfully'
        })

    except Exception as e:

        return JsonResponse({
            'success': False,
            'message': str(e)
        })


# =========================
# DELETE CART ITEM
# =========================

@login_required
def delete_cart_item(request, cart_id):

    cart_item = get_object_or_404(

        Cart,
        id=cart_id,
        user=request.user

    )

    cart_item.delete()

    return JsonResponse({

        'success': True

    })


# =========================
# ADDRESS PAGE
# =========================

@login_required
def address(request):

    previous_addresses = UserAddress.objects.filter(
        user=request.user
    )

    if request.method == 'POST':

        selected_address_id = request.POST.get(
            'selected_address'
        )

        if selected_address_id:

            address_obj = get_object_or_404(
                UserAddress,
                id=selected_address_id,
                user=request.user
            )

            address_data = {
                'name': address_obj.name,
                'phone': address_obj.phone,
                'area': address_obj.area,
                'city': address_obj.city,
                'landmark': address_obj.landmark,
                'district': address_obj.district,
                'zipcode': address_obj.zipcode,
            }

        else:

            address_data = {
                'name': request.POST.get('name'),
                'phone': request.POST.get('phone'),
                'area': request.POST.get('area'),
                'city': request.POST.get('city'),
                'landmark': request.POST.get('landmark'),
                'district': request.POST.get('district'),
                'zipcode': request.POST.get('zipcode'),
            }

            UserAddress.objects.create(
                user=request.user,
                **address_data
            )

        request.session['delivery_address'] = address_data

        return redirect('orders:confirm_order')

    return render(request, 'address.html', {
        'previous_addresses': previous_addresses
    })


# =========================
# CONFIRM ORDER PAGE
# =========================

@login_required
def confirm_order(request):

    address = request.session.get('delivery_address')

    if not address:
        return redirect('orders:address')

    cart_items = Cart.objects.filter(
        user=request.user
    ).select_related('food_item', 'food_item__category')

    subtotal = Decimal('0.00')
    for item in cart_items:
        subtotal += item.total_price

    delivery_fee = Decimal('40.00')
    gst = subtotal * Decimal('0.05')
    grand_total = subtotal + delivery_fee + gst

    return render(request, 'confirm_order.html', {
        'address': address,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'gst': gst,
        'grand_total': grand_total
    })


# =========================
# PLACE ORDER
# =========================

@login_required
@require_POST
def place_order(request):
    try:
        # Get address from session
        address = request.session.get('delivery_address')
        if not address:
            return JsonResponse({
                'success': False,
                'message': 'Please select a delivery address first'
            })

        # Get cart items
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return JsonResponse({
                'success': False,
                'message': 'Cart is empty'
            })

        # Get payment method from request
        payment_method = 'Cash on Delivery'
        try:
            data = json.loads(request.body)
            if data.get('payment_method'):
                payment_method = data.get('payment_method')
        except:
            pass

        # Calculate totals
        subtotal = Decimal('0')
        for item in cart_items:
            item_total = Decimal(str(item.food_item.price)) * item.quantity
            subtotal += item_total

        delivery_fee = Decimal('40.00')
        gst_amount = (subtotal * Decimal('5')) / Decimal('100')
        total_price = subtotal + delivery_fee + gst_amount

        # Create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total_price,
            payment_method=payment_method,
            delivery_fee=delivery_fee,
            gst_amount=gst_amount,
            payment_status=False,
            status='Pending'
        )

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                food_item=item.food_item,
                quantity=item.quantity,
                price=item.food_item.price
            )

        # Clear cart
        cart_items.delete()

        # Clear session
        request.session.pop('delivery_address', None)

        return JsonResponse({
            'success': True,
            'redirect_url': '/my-orders/',
            'order_id': order.id,
            'message': 'Order placed successfully!'
        })

    except Exception as e:
        print(f"[ERROR] Place order failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Order failed: {str(e)}'
        }, status=400)


# =========================
# MY ORDERS
# =========================

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        'items__food_item'
    ).order_by('-created_at')

    return render(request, 'my_orders.html', {
        'orders': orders
    })


# =========================
# DELETE ORDER
# =========================

@login_required
@require_POST
def delete_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order.delete()

    return JsonResponse({
        'success': True,
        'message': 'Order deleted successfully'
    })


# =========================
# STRIPE PAYMENT
# =========================

@login_required
@require_POST
def create_stripe_session(request):

    address = request.session.get('delivery_address')

    if not address:
        return JsonResponse({
            'success': False,
            'message': 'Please select a delivery address first'
        })

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return JsonResponse({
            'success': False,
            'message': 'Cart is empty'
        })

    if not settings.STRIPE_SECRET_KEY or settings.STRIPE_SECRET_KEY == 'your_secret_key':
        return JsonResponse({
            'success': False,
            'message': 'Payment gateway is not configured. Please contact support or use Cash on Delivery.'
        })

    try:
        total_price = sum(
            item.food_item.price * item.quantity
            for item in cart_items
        )

        delivery_fee = Decimal('40.00')
        gst = total_price * Decimal('0.05')
        grand_total = total_price + delivery_fee + gst

        # Create order first
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=grand_total,
            payment_method='Online Payment',
            delivery_fee=delivery_fee,
            gst_amount=gst,
            payment_status=False
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                food_item=item.food_item,
                quantity=item.quantity,
                price=item.food_item.price
            )

        line_items = []

        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': item.food_item.name,
                    },
                    'unit_amount': int(
                        item.food_item.price * 100
                    ),
                },
                'quantity': item.quantity,
            })

        # Add delivery fee
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'Delivery Fee',
                },
                'unit_amount': int(40 * 100),
            },
            'quantity': 1,
        })

        # Add GST
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'GST (5%)',
                },
                'unit_amount': int(gst * 100),
            },
            'quantity': 1,
        })

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=request.user.email,
            line_items=line_items,
            mode='payment',
            metadata={'order_id': order.id},
            success_url=request.build_absolute_uri(
                f'/payment-success/{order.id}/'
            ),
            cancel_url=request.build_absolute_uri(
                '/cart/'
            ),
        )

        return JsonResponse({
            'success': True,
            'session_url': session.url
        })

    except stripe.error.CardError as e:
        order.delete()
        return JsonResponse({
            'success': False,
            'message': f'Card error: {e.user_message}'
        })

    except stripe.error.RateLimitError as e:
        order.delete()
        return JsonResponse({
            'success': False,
            'message': 'Too many requests. Please try again later.'
        })

    except stripe.error.InvalidRequestError as e:
        order.delete()
        return JsonResponse({
            'success': False,
            'message': f'Invalid request: {str(e)}'
        })

    except stripe.error.AuthenticationError as e:
        order.delete()
        return JsonResponse({
            'success': False,
            'message': 'Payment gateway authentication failed. Please try again later.'
        })

    except Exception as e:
        order.delete()
        return JsonResponse({
            'success': False,
            'message': f'Payment error: {str(e)}'
        })


@login_required
def payment_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order.payment_status = True
    order.status = 'Preparing'
    order.save()

    Cart.objects.filter(user=request.user).delete()

    request.session.pop('delivery_address', None)

    messages.success(
        request,
        "Payment successful! Your order has been placed."
    )

    return redirect('orders:my_orders')


# =========================
# DELETE ADDRESS
# =========================

@login_required
@require_POST
def delete_address(request, address_id):

    address = get_object_or_404(
        UserAddress,
        id=address_id,
        user=request.user
    )

    address.delete()

    return JsonResponse({
        'success': True,
        'message': 'Address deleted successfully'
    })



