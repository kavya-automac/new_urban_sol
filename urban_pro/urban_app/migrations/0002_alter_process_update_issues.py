# Generated by Django 4.2.7 on 2023-11-16 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urban_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process_update',
            name='issues',
            field=models.TextField(blank=True, null=True),
        ),
    ]
