# Generated by Django 3.1 on 2022-04-20 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20220412_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='header_image',
            field=models.ImageField(blank=True, upload_to='images/', verbose_name='Header Image'),
        ),
    ]
