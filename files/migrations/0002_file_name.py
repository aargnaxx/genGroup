# Generated by Django 3.2.9 on 2022-01-14 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]