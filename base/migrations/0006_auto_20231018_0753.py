# Generated by Django 3.2.22 on 2023-10-18 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20231018_0617'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='catatan',
            field=models.TextField(default=''),
        ),
    ]
