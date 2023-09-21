from rest_framework import serializers

from .models import Item, Saw
from .api.serializers import SawModelSerializer


class MenuModelSerializer(serializers.ModelSerializer):
    saws = serializers.SerializerMethodField('get_saws')
    class Meta:
        model = Item
        fields = ['id', 'nama_item', 'kategori', 'harga', 'nilai', 'stok', 'gambar', 'saws']

    def get_saws(self, obj):
        saws = obj.saw_set.all()
        return SawModelSerializer(saws, many=True).data