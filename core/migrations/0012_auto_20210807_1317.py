# Generated by Django 2.2 on 2021-08-07 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_productimage_productid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='productId',
            field=models.IntegerField(db_column='productId', null=True, unique=True),
        ),
    ]
