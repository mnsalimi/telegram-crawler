# Generated by Django 4.1 on 2022-08-08 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0012_alter_post_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='views',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]