# Generated by Django 3.1 on 2022-04-20 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20220420_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='header',
            field=models.ImageField(blank=True, null=True, upload_to='blog/%Y/%m/%d', verbose_name='Header'),
        ),
    ]