# Generated by Django 3.2.9 on 2024-01-14 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstoreapp', '0004_auto_20240114_0437'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='linkedin_url',
            field=models.URLField(blank=True),
        ),
    ]