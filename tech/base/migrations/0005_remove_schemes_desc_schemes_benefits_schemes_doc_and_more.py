# Generated by Django 5.0.1 on 2024-02-16 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_schemes_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schemes',
            name='desc',
        ),
        migrations.AddField(
            model_name='schemes',
            name='benefits',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='schemes',
            name='doc',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='schemes',
            name='duration',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='schemes',
            name='elibilty',
            field=models.TextField(null=True),
        ),
    ]
