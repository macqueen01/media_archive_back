# Generated by Django 4.0.6 on 2022-10-16 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample_backend', '0015_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
