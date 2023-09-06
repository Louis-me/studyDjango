# Generated by Django 3.1.3 on 2023-08-31 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0006_auto_20230829_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='suite',
        ),
        migrations.CreateModel(
            name='SuiteSetCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_id', models.IntegerField(null=True)),
                ('suite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TestModel.suite')),
            ],
        ),
    ]