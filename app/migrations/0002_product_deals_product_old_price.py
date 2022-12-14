# Generated by Django 4.1 on 2022-10-03 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='deals',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
    ]
