# Generated by Django 3.2.18 on 2023-03-23 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='')),
            ],
        ),
    ]
