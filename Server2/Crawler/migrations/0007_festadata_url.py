# Generated by Django 2.1.1 on 2018-09-12 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crawler', '0006_remove_festadata_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='festadata',
            name='url',
            field=models.CharField(default=0, max_length=128),
            preserve_default=False,
        ),
    ]
