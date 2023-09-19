from django.db import models


# class Rating(models.Model):
#     nilai = models.FloatField()
#     jumlah_bintang = models.IntegerField()
#     jumlah_penilai = models.IntegerField()

#     def __str__(self):
#         return self.nilai

class Item(models.Model):
    nama_item = models.CharField(max_length=50)
    kategori = models.CharField(max_length=20)
    harga = models.IntegerField()
    # id_nilai = models.ForeignKey(Rating, on_delete=models.CASCADE)
    gambar = models.ImageField(null=True, blank=True)

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
