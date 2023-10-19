from django.db import models
from django.conf import settings

from account.models import User


class Item(models.Model):
    nama_item = models.CharField(max_length=50)
    kategori = models.CharField(max_length=20)
    harga = models.IntegerField()
    deskripsi = models.TextField(default="")
    gambar = models.ImageField(null=True, blank=True, upload_to='images/')
    stok = models.CharField(max_length=20, default='tidak tersedia')
    nilai = models.IntegerField(default=0)
    jumlah_bintang = models.IntegerField(default=0)
    jumlah_penilai = models.IntegerField(default=0)

    def __str__(self):
        return self.nama_item


class Kriteria(models.Model):
    nama_kriteria = models.CharField(max_length=50)
    atribut = models.CharField(max_length=50)
    bobot = models.FloatField()
    pertanyaan = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nama_kriteria


class Subkriteria(models.Model):
    kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE)
    nama_subkriteria = models.CharField(max_length=50)

    def __str__(self):
        return self.nama_subkriteria


class Saw(models.Model):
    alternatif = models.ForeignKey(Item, on_delete=models.CASCADE)
    subkriteria = models.ForeignKey(Subkriteria, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.alternatif} - {self.subkriteria}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('keranjang', 'Keranjang'),
        ('dikonfirmasi', 'Dikonfirmasi'),
        ('selesai', 'Selesai'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waktu_pemesanan = models.DateTimeField(auto_now=True)
    total_pembayaran = models.IntegerField(default=0)
    is_notified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.user.full_name} - {self.waktu_pemesanan}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    catatan = models.TextField(default='')
    jumlah_pesanan = models.IntegerField(default=0)
    total_harga = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.item.nama_item} - {self.order.user.full_name}'