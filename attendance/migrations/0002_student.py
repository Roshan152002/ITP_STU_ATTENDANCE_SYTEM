# Generated by Django 5.1.6 on 2025-02-24 03:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='student_model', serialize=False, to='attendance.user')),
                ('roll_no', models.CharField(max_length=10, unique=True)),
                ('batch_name', models.CharField(max_length=100)),
                ('phone_no', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('enrollment_date', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
            ],
            options={
                'ordering': ['roll_no'],
            },
        ),
    ]
