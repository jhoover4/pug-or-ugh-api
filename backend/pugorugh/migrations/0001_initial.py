# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-10-11 02:38
from __future__ import unicode_literals

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
            name='Dog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image_filename', models.ImageField(upload_to='')),
                ('breed', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('u', 'Unknown')], max_length=1)),
                ('size', models.CharField(choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('xl', 'Extra Large'), ('u', 'Unknown')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserDog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('l', 'Liked'), ('d', 'Disliked')], max_length=1)),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pugorugh.Dog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=15)),
                ('age', models.CharField(max_length=15)),
                ('size', models.CharField(max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
