# Generated by Django 4.1.11 on 2023-10-04 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentimentfeature',
            name='text',
            field=models.CharField(max_length=5),
        ),
    ]
