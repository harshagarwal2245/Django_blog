# Generated by Django 3.1 on 2022-04-20 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20220420_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='header',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
