# Generated by Django 3.1.5 on 2021-03-02 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20210301_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_amount', models.FloatField(default=0)),
                ('bid_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_item_id', to='auctions.listings')),
                ('bid_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
