from . import signals
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .services.flash_sale import check_flash_sale, FlashSaleListCreteView
from .services.product_view_history import ProductViewHistoryCreate
from .services.replanish_stock import admin_replenish_stock
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sale/', FlashSaleListCreteView.as_view(), name='sale'),
    path('check-sale/<int:product_id>/', check_flash_sale, name='check-flash-sale'),
    path('product-view/', ProductViewHistoryCreate.as_view(), name='product-view-history-create'),
    path('admin/replenish_stock/<int:product_id>/<int:amount>', admin_replenish_stock, name='admin_replenish_stock'),

]
