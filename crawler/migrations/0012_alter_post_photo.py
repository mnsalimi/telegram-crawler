# Generated by Django 4.1 on 2022-08-07 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0011_alter_post_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
