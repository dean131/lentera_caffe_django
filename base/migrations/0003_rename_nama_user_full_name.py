# Generated by Django 4.2.6 on 2023-10-13 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_order_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='nama',
            new_name='full_name',
        ),
    ]