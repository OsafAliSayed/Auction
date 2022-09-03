# Generated by Django 4.0.2 on 2022-05-15 11:23

import auctions.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_item_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='lastBidder',
            field=models.ForeignKey(default=auctions.models.Item.default_Bidder, on_delete=django.db.models.deletion.CASCADE, related_name='last_Bidder', to=settings.AUTH_USER_MODEL),
        ),
    ]
