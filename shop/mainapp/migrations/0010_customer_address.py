# Generated by Django 3.2.9 on 2021-12-07 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_alter_dog_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес'),
        ),
    ]
