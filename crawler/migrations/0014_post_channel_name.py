# Generated by Django 4.1 on 2022-08-08 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0013_alter_post_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='channel_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
