from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    CartViewSet,
    OrderViewSet,
    AdminOrderViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"admin/orders", AdminOrderViewSet, basename="admin-orders")

urlpatterns = [
    path("api/", include(router.urls)),
]
