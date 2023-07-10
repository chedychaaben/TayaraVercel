# Generated by Django 4.2.3 on 2023-07-10 21:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tayara', '0009_annonce_is_ontayaranow'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnonceOnTayaraNow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annonce', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AnnonceOnTayaraNow_user_Annonce', to='tayara.annonce')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AnnonceOnTayaraNow_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
