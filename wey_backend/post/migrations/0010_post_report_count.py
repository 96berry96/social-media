# Generated by Django 5.0.1 on 2024-05-03 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_post_reported_by_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='report_count',
            field=models.IntegerField(default=0),
        ),
    ]
