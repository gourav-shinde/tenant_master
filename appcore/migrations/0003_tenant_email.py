# Generated by Django 3.1.1 on 2020-11-17 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appcore', '0002_auto_20201107_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
