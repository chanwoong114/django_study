# Generated by Django 3.1.7 on 2023-04-10 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eithers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pick',
            field=models.BooleanField(default=False),
        ),
    ]
