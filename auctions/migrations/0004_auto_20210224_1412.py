# Generated by Django 3.1.5 on 2021-02-24 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210222_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='List_time_made',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='listings',
            name='List_image_url',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]