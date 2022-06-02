from rest_framework import serializers

from .models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']



class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = Stock.objects.create(**validated_data)
        # stock = super().create(validated_data)
        for position in positions:
            # StockProduct.create(stock=stock, position=position)
            StockProduct.objects.create(stock=stock, **position)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        # print(stock)
        for position in positions:
            # print(position)
            items = StockProduct.objects.filter(stock=stock)
            for item in items:
                if item.product == position.get('product'):
                    item.quantity = position.get('quantity')
                    item.price = position.get('price')
                    item.save()
                print(item)

        return stock
