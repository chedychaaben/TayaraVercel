# Generated by Django 4.2.3 on 2023-07-10 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_account_ontayara_ads_now'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='onTayara_ads_now',
        ),
    ]