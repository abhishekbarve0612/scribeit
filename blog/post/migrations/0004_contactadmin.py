# Generated by Django 2.2 on 2020-05-30 06:27

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_remove_post_dislikes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('emailid', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=120)),
                ('message', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
        ),
    ]