# Generated by Django 3.2.9 on 2021-11-16 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20211116_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dogforsale',
            name='age',
            field=models.TextField(max_length=10, verbose_name='Возраст'),
        ),
        migrations.AlterField(
            model_name='ourdog',
            name='age',
            field=models.TextField(max_length=10, verbose_name='Возраст'),
        ),
    ]
