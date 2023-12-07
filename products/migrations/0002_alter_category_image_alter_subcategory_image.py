# Generated by Django 4.2.7 on 2023-11-22 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images/categories/%y%m%d'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images/subcategories/%y%m%d'),
        ),
    ]