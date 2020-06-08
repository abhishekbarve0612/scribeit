# Generated by Django 2.2 on 2020-06-06 12:55

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=100)),
                ('address', models.CharField(default='', max_length=150)),
                ('website', models.URLField(default='', null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=20)),
                ('mobileNumber', models.IntegerField(default=0, null=True)),
                ('profilePic', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('coverPic', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('contactDetailsVisible', models.BooleanField(default=False)),
                ('profileDetailsVisible', models.BooleanField(default=True)),
                ('fav_music', models.CharField(blank=True, max_length=120, null=True)),
                ('fav_books', models.CharField(blank=True, max_length=120, null=True)),
                ('fav_movie', models.CharField(blank=True, max_length=120, null=True)),
                ('skills', models.CharField(blank=True, max_length=120, null=True)),
                ('interest', models.CharField(blank=True, max_length=120, null=True)),
                ('facebook_url', models.URLField(blank=True, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('twitter_url', models.URLField(blank=True, null=True)),
                ('instagram_url', models.URLField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
