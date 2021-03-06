# Generated by Django 3.2.9 on 2022-01-17 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_file_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisFile',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='files/')),
            ],
        ),
        migrations.CreateModel(
            name='ResultFile',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='files/')),
            ],
        ),
        migrations.DeleteModel(
            name='File',
        ),
    ]
