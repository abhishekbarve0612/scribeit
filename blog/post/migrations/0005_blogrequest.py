# Generated by Django 2.2 on 2020-05-30 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_contactadmin'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=120)),
                ('userRequest', models.CharField(max_length=150)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
