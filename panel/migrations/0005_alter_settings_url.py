# Generated by Django 3.2.16 on 2022-10-30 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0004_auto_20221030_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='url',
            field=models.URLField(blank=True, default='site.com', null=True, verbose_name='website url'),
        ),
    ]
