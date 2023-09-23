# Generated by Django 4.2.5 on 2023-09-22 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_item', models.CharField(max_length=50)),
                ('kategori', models.CharField(max_length=20)),
                ('harga', models.IntegerField()),
                ('gambar', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('stok', models.CharField(default='tidak tersedia', max_length=20)),
                ('nilai', models.IntegerField(default=0)),
                ('jumlah_bintang', models.IntegerField(default=0)),
                ('jumlah_penilai', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Kriteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_kriteria', models.CharField(max_length=50)),
                ('atribut', models.CharField(max_length=50)),
                ('bobot', models.FloatField()),
                ('pertanyaan', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu_pemesanan', models.DateTimeField()),
                ('total_pembayaran', models.IntegerField()),
                ('is_notified', models.BooleanField(default=False)),
                ('status', models.CharField(max_length=20)),
                ('qr_code', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('nama', models.CharField(max_length=255)),
                ('telepon', models.CharField(blank=True, max_length=20, null=True)),
                ('role', models.CharField(max_length=20)),
                ('foto_profil', models.ImageField(blank=True, null=True, upload_to='')),
                ('date_joined', models.DateField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateField(auto_now=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subkriteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_subkriteria', models.CharField(max_length=50)),
                ('kriteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.kriteria')),
            ],
        ),
        migrations.CreateModel(
            name='Saw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternatif', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.item')),
                ('subkriteria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.subkriteria')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jumlah_pesanan', models.IntegerField()),
                ('total_harga', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user'),
        ),
    ]
