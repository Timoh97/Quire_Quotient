# Generated by Django 3.2.9 on 2024-01-14 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstoreapp', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='facebook_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='instagram_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='profession',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='twitter_url',
            field=models.URLField(blank=True),
        ),
    ]
