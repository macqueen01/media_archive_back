# Generated by Django 4.0.6 on 2022-10-16 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sample_backend', '0005_remove_user_image_remove_user_name_user_is_active_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='name',
        ),
    ]
