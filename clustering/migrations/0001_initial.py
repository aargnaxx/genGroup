# Generated by Django 3.2.9 on 2022-01-14 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_file', models.CharField(max_length=256)),
                ('result_file', models.CharField(max_length=256)),
                ('seq_length', models.IntegerField()),
                ('decrement_range', models.IntegerField()),
                ('increment_range', models.IntegerField()),
            ],
        ),
    ]