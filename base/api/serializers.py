from rest_framework import serializers

from base.models import Saw, Item, Kriteria, Subkriteria, Order, OrderItem, Notifikasi


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
    nama_item = serializers.SerializerMethodField('get_nama_item')
    gambar = serializers.SerializerMethodField('get_gambar')

    class Meta:
         model = OrderItem
         fields = '__all__'

    def get_nama_item(self, obj):
        nama_item = obj.item.nama_item
        return nama_item
    
    def get_gambar(self, obj):
        item = ItemModelSerializer(obj.item, context=self.context).data
        return item['gambar']


class NotifikasiModelSerializer(serializers.ModelSerializer):
    class Meta:
         model = Notifikasi
         fields = '__all__'


class OrderModelSerializer(serializers.ModelSerializer):
    order_item = serializers.SerializerMethodField('get_order_item')

    class Meta:
         model = Order
         fields = '__all__'

    def get_order_item(self, obj):
        order_item = obj.orderitem_set.all()
        return OrderItemModelSerializer(order_item, many=True, context=self.context).data


class PertanyaanModelSerializer(serializers.ModelSerializer):
    subkriteria = serializers.SerializerMethodField('get_subkriteria')

    class Meta:
         model = Kriteria
         fields = ['nama_kriteria', 'pertanyaan', 'subkriteria']

    def get_subkriteria(self, obj):
        subkriterias = obj.subkriteria_set.all()
        serializer = SubkriteriaModelSerializer(instance=subkriterias, many=True)
        return serializer.data
