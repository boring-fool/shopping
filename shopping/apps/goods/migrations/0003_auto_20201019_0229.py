# Generated by Django 2.2 on 2020-10-18 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20201015_1955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sku',
            name='default_image_url',
        ),
        migrations.AddField(
            model_name='sku',
            name='default_image',
            field=models.ImageField(blank=True, default='', max_length=200, null=True, upload_to='', verbose_name='默认图片'),
        ),
    ]