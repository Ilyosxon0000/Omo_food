# Generated by Django 4.2.7 on 2023-12-18 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Each_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('total_price', models.FloatField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(blank=True, null=True)),
                ('longitude', models.CharField(blank=True, max_length=200, null=True)),
                ('latitude', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.FloatField(default=0)),
                ('delivery_status', models.CharField(choices=[('QABUL QILINDI', 'QABUL QILINDI'), ('YETKAZILMOQDA', 'YETKAZILMOQDA'), ('YETKAZILDI', 'YETKAZILDI')], default='QABUL QILINDI', max_length=50)),
                ('address_status', models.CharField(choices=[('CITY_IN', 'CITY_IN'), ('CITY_OUT', 'CITY_OUT')], default='CITY_IN', max_length=50)),
                ('payment_method', models.CharField(choices=[('NAQD', 'NAQD'), ("TO'LOV TIZIMI", "TO'LOV TIZIMI")], default='NAQD', max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('each_products', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='order.each_product')),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='order.location')),
            ],
        ),
    ]
