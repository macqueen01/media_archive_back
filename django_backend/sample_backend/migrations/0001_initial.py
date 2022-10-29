# Generated by Django 3.2.14 on 2022-10-27 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('username', models.CharField(max_length=120, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('affiliation', models.CharField(max_length=40)),
                ('position', models.CharField(max_length=20)),
                ('standing', models.CharField(max_length=20)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('is_superuser', models.IntegerField(blank=True, null=True)),
                ('is_active', models.IntegerField(blank=True, null=True)),
                ('is_staff', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'auth_user',
            },
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_type', models.CharField(max_length=10)),
                ('uploader', models.CharField(max_length=10)),
                ('associate', models.CharField(max_length=10)),
                ('location', models.CharField(max_length=10)),
                ('collected', models.IntegerField(default=0)),
                ('private', models.IntegerField(default=0)),
                ('attendee', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('src', models.ImageField(upload_to='image/%Y%m%d')),
            ],
        ),
        migrations.CreateModel(
            name='DocCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField()),
                ('content', models.TextField()),
                ('private', models.IntegerField()),
                ('form', models.IntegerField(default=2)),
                ('form2_accessed_by', models.ManyToManyField(related_name='access_to_form2', to='sample_backend.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImageCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField()),
                ('content', models.TextField()),
                ('private', models.IntegerField()),
                ('form', models.IntegerField(default=0)),
                ('produced', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField()),
                ('content', models.TextField()),
                ('private', models.IntegerField()),
                ('form', models.IntegerField(default=4)),
                ('construction_date', models.DateTimeField(default=None, null=True)),
                ('form4_accessed_by', models.ManyToManyField(related_name='access_to_form4', to='sample_backend.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Personel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField()),
                ('content', models.TextField()),
                ('private', models.IntegerField()),
                ('form', models.IntegerField(default=3)),
                ('birth_date', models.DateTimeField(default=None, null=True)),
                ('prefix', models.CharField(max_length=20, null=True)),
                ('affiliation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sample_backend.location')),
                ('connected_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sample_backend.user')),
                ('form3_accessed_by', models.ManyToManyField(related_name='access_to_form3', to='sample_backend.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField()),
                ('content', models.TextField()),
                ('private', models.IntegerField()),
                ('form', models.IntegerField(default=1)),
                ('produced', models.IntegerField()),
                ('affiliation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_affiliation_in_form1', to='sample_backend.location')),
                ('associate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='associated_in_form1', to='sample_backend.personel')),
                ('attendee', models.ManyToManyField(related_name='appears_in_form1', to='sample_backend.Personel')),
                ('form1_accessed_by', models.ManyToManyField(related_name='access_to_form1', to='sample_backend.User')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_location_in_form1', to='sample_backend.location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('name', models.CharField(max_length=300)),
                ('extension', models.CharField(max_length=20)),
                ('url', models.FileField(upload_to='stream/video/%Y%m%d')),
                ('referenced_in', models.ManyToManyField(related_name='include', to='sample_backend.VideoCase')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImageMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('name', models.CharField(max_length=300)),
                ('extension', models.CharField(max_length=20)),
                ('url', models.ImageField(upload_to='stream/image/%Y%m%d')),
                ('image_of', models.ManyToManyField(related_name='view', to='sample_backend.Location')),
                ('profile_of', models.ManyToManyField(related_name='profile', to='sample_backend.Personel')),
                ('referenced_in', models.ManyToManyField(related_name='include', to='sample_backend.ImageCase')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='imagecase',
            name='affiliation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_affiliation_in_form0', to='sample_backend.location'),
        ),
        migrations.AddField(
            model_name='imagecase',
            name='associate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='associated_in_form0', to='sample_backend.personel'),
        ),
        migrations.AddField(
            model_name='imagecase',
            name='attendee',
            field=models.ManyToManyField(related_name='appears_in_form0', to='sample_backend.Personel'),
        ),
        migrations.AddField(
            model_name='imagecase',
            name='form0_accessed_by',
            field=models.ManyToManyField(related_name='access_to_form0', to='sample_backend.User'),
        ),
        migrations.AddField(
            model_name='imagecase',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_location_in_form0', to='sample_backend.location'),
        ),
        migrations.CreateModel(
            name='DocMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('name', models.CharField(max_length=300)),
                ('extension', models.CharField(max_length=20)),
                ('url', models.FileField(upload_to='stream/document/%Y%m%d')),
                ('referenced_in', models.ManyToManyField(related_name='include', to='sample_backend.DocCase')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='doccase',
            name='referenced_personel',
            field=models.ManyToManyField(related_name='referenced_in', to='sample_backend.Personel'),
        ),
        migrations.AddField(
            model_name='doccase',
            name='writer',
            field=models.ManyToManyField(related_name='wrote', to='sample_backend.Personel'),
        ),
    ]
