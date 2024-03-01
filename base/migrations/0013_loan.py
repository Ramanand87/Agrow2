# Generated by Django 5.0.1 on 2024-02-26 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_schemes_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('img', models.ImageField(upload_to='loan')),
                ('purpose', models.TextField()),
                ('eligibility', models.TextField()),
            ],
        ),
    ]
