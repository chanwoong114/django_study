# Generated by Django 3.2 on 2022-12-26 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='result',
            name='file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
