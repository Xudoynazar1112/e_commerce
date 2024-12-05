from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers

from .product import Product
from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r'^\+9989\d{9}$',
    message="Phone number must be entered in the format: '+998xxxxxxxxx'. Up to 15 digits allowed."
)


class Order(models.Model):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True, null=True)

    def set_status(self, new_status):
        if new_status not in self.STATUS_CHOICES:
            raise ValueError('Invalid status')
        self.status = new_status
        self.save()

    def is_transition_allowed(self, new_status):
        allowed_transitions = {
            self.PENDING: [self.PROCESSING, self.CANCELED],
            self.PROCESSING: [self.SHIPPED, self.CANCELED],
            self.SHIPPED: [self.DELIVERED, self.CANCELED],
        }

        return new_status in allowed_transitions.get(self.status, [])

    def __str__(self):
        return f'Order ({self.product.name} by {self.customer.username})'

    def validate_quantity(self, value):
        try:
            product_id = self.initial_data['product']
            product = Product.objects.get(id=product_id)
            if value > product.stock:
                raise serializers.ValidationError('Not enough items in stock.')
            elif value < 1:
                raise serializers.ValidationError('Quantity must be at least 1.')
            return True

        except ObjectDoesNotExist:
            raise serializers.ValidationError('Product does not exist.')

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        product = order.product
        product.stock -= order.quantity
        product.save()
        self.send_confirmation_email(order)
        return order

    def send_confirmation_email(self, order):
        print(f"Send confirmation email for order {order.id}")
