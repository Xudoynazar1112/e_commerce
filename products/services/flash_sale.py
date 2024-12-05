from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view

from products.models import FlashSale, Product, ProductViewHistory


class FlashSaleListCreteView(generics.ListCreateAPIView):
    queryset = FlashSale.objects.all()

    class FlashSaleSerializer(serializers.ModelSerializer):
        class Meta:
            model = FlashSale
            fields = '__all__'

    serializer_class = FlashSaleSerializer


@api_view(['GET'])
def check_flash_sale(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    user_viewed = ProductViewHistory.objects.filter(product=product, user=request.user).exists()

    upcoming_flash_sale = FlashSale.objects.filter(product=product,
                                                   start_time__lte=datetime.now() + timedelta(hours=48)).first()
    if user_viewed and upcoming_flash_sale:
        discount = upcoming_flash_sale.discount_percentage
        start_time = upcoming_flash_sale.start_time
        end_time = upcoming_flash_sale.end_time
        return Response({
            "message": f"This product will be on a {discount}% off discount sale!",
            "start_time": start_time,
            "end_time": end_time
        })
    else:
        return Response({"message": "No upcoming flash sale for this product"})
