# Generated by Django 4.2.3 on 2023-09-04 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_account_ontayara_ads_now'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='login_bytes_code',
        ),
        migrations.AddField(
            model_name='account',
            name='login_hex_code',
            field=models.CharField(blank=True, max_length=750, null=True),
        ),
    ]
