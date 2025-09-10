from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db import transaction
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
)

# ---------- Swagger Auth Header ----------
auth_header = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="Bearer token (format: Bearer <access_token>)",
    type=openapi.TYPE_STRING,
    required=True
)


# ---------- CATEGORY ----------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_description="List all categories")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[auth_header],
        operation_description="Create a new category (Admin only)"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


# ---------- PRODUCT ----------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).order_by("-created_at")
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [AllowAny]

    @swagger_auto_schema(operation_description="List all active products")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# ---------- CART ----------
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[auth_header],
        operation_description="Retrieve logged-in user's cart",
        responses={200: CartSerializer}
    )
    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[auth_header],
        operation_description="Add a product to the cart",
        request_body=CartItemSerializer,
        responses={201: CartSerializer, 400: "Invalid data"}
    )
    def create(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"price": product.price, "quantity": quantity},
        )
        if not created:
            item.quantity += quantity
            item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        manual_parameters=[auth_header],
        operation_description="Update quantity of a cart item",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"quantity": openapi.Schema(type=openapi.TYPE_INTEGER)}
        ),
        responses={200: CartSerializer, 404: "Item not found"}
    )
    def update(self, request, pk=None):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        try:
            item = cart.items.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

        quantity = request.data.get("quantity")
        if quantity and int(quantity) > 0:
            item.quantity = int(quantity)
            item.save()
        else:
            item.delete()

        return Response(CartSerializer(cart).data)

    @swagger_auto_schema(
        manual_parameters=[auth_header],
        operation_description="Remove a product from the cart",
        responses={200: CartSerializer, 404: "Item not found"}
    )
    def destroy(self, request, pk=None):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        try:
            item = cart.items.get(pk=pk)
            item.delete()
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

        return Response(CartSerializer(cart).data)


# ---------- ORDER ----------
class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[auth_header],
        operation_description="List all orders of the logged-in user",
        responses={200: OrderSerializer(many=True)}
    )
    def list(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        return Response(OrderSerializer(orders, many=True).data)

    @swagger_auto_schema(
        manual_parameters=[auth_header],
        operation_description="Place a new order from the cart",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "shipping_address": openapi.Schema(type=openapi.TYPE_STRING),
                "phone": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["shipping_address", "phone"],  # 👈 required fields clear kar diye
        ),
        responses={201: OrderSerializer, 400: "Cart is empty"}
    )
    @transaction.atomic
    def create(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        # ⚡ status force karna (user input ignore)
        order = Order.objects.create(
            user=request.user,
            shipping_address=request.data.get("shipping_address", ""),
            phone=request.data.get("phone", ""),
            status="PENDING",  # 👈 force default PENDING
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price,
            )
            item.product.stock -= item.quantity
            item.product.save()

        order.calculate_total()
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=201)



# ---------- ADMIN ORDER MANAGEMENT ----------
class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        manual_parameters=[auth_header],
        operation_description="List all orders (Admin only)"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[auth_header],
        operation_description="Replace full order details (Admin only)"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[auth_header],
        operation_description="Cancel an order (Admin only)"
    )
    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        order.status = "CANCELLED"   # 👈 soft delete instead of hard delete
        order.save()
        return Response({"status": "Order cancelled"}, status=200)

    @swagger_auto_schema(
        manual_parameters=[auth_header],
        operation_description="Update only specific fields (e.g., order status) (Admin only)"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
