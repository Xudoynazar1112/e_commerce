from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from products.models import Order, Product


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'product', 'total_price', 'customer', 'quantity', 'created_at', 'phone_number']

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity
