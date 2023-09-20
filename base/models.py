from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, 
    AbstractBaseUser,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, full_name=None,  *args, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), full_name=full_name, *args, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(email=email, password=password, full_name=full_name,)
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    GENDER_CHOICES = [
        ('laki-laki', 'Laki-laki'),
        ('perempuan', 'Perempuan'),
    ]

    email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True) 
    profile_picture = models.ImageField(blank=True, null=True)

    date_joined = models.DateField(verbose_name='date joined', auto_now_add=True,)
    last_login = models.DateField(verbose_name='last login', auto_now=True,)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Item(models.Model):
    nama_item = models.CharField(max_length=50)
    kategori = models.CharField(max_length=20)
    harga = models.IntegerField()
    gambar = models.ImageField(null=True, blank=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waktu_pemesanan = models.DateTimeField()
    total_pembayaran = models.IntegerField()
    is_notified = models.BooleanField(default=False)
    status = models.CharField(max_length=20)
    qr_code = models.CharField(max_length=250)

    def __str__(self):
        return f'Dipesan oleh {self.user.full_name}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    jumlah_pesanan = models.IntegerField()
    total_harga = models.IntegerField()

    def __str__(self):
        return 