# Generated by Django 4.0.6 on 2022-10-16 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample_backend', '0006_rename_username_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
