# Generated by Django 4.2.3 on 2023-07-10 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_account_last_time_triggered'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='onTayara_ads_now',
            field=models.CharField(blank=True, default='[]', null=True),
        ),
    ]