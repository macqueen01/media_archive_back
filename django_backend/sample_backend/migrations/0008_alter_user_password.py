# Generated by Django 4.0.6 on 2022-10-16 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample_backend', '0007_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='placeholder', max_length=128),
        ),
    ]
