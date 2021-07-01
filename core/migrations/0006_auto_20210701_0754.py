# Generated by Django 2.2 on 2021-07-01 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210701_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(db_column='Name', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='owner',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]
