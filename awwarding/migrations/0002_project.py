# Generated by Django 3.2.7 on 2021-09-21 14:49

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('awwarding', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('proj_img', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Project screenshot')),
                ('desc', models.TextField()),
                ('link', models.URLField()),
                ('post_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='awwarding.profile')),
            ],
            options={
                'ordering': ['-post_date'],
            },
        ),
    ]