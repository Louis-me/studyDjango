# Generated by Django 3.1.3 on 2023-08-29 02:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0005_auto_20230829_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='suite',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='suite',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
