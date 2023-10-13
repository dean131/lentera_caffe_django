from rest_framework import serializers

from base.models import Saw, Item, Kriteria, Subkriteria, Order, OrderItem


class SawModelSerializer(serializers.ModelSerializer):
    class Meta:
         model = Saw
         fields = '__all__'


class ItemModelSerializer(serializers.ModelSerializer):
    class Meta:
         model = Item
         fields = '__all__'


class KriteriaModelSerializer(serializers.ModelSerializer):
    class Meta:
         model = Kriteria
         fields = '__all__'


class SubkriteriaModelSerializer(serializers.ModelSerializer):
    class Meta:
         model = Subkriteria
         fields = '__all__'


class OrderItemModelSerializer(serializers.ModelSerializer):

    class Meta:
         model = OrderItem
         fields = '__all__'


class OrderModelSerializer(serializers.ModelSerializer):
    order_item = serializers.SerializerMethodField('get_order_item')

    class Meta:
         model = Order
         fields = '__all__'

    def get_order_item(self, obj):
        order_item = obj.orderitem_set.all()
        return OrderItemModelSerializer(order_item, many=True).data


class PertanyaanModelSerializer(serializers.ModelSerializer):
    subkriteria = serializers.SerializerMethodField('get_subkriteria')

    class Meta:
         model = Kriteria
         fields = ['nama_kriteria', 'pertanyaan', 'subkriteria']

    def get_subkriteria(self, obj):
        subkriterias = obj.subkriteria_set.all()
        serializer = SubkriteriaModelSerializer(instance=subkriterias, many=True)
        return serializer.data
