# Generated by Django 4.2.5 on 2023-09-20 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_order_user_item_jumlah_bintang_item_jumlah_penilai_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_notified',
            field=models.BooleanField(default=False),
        ),
    ]