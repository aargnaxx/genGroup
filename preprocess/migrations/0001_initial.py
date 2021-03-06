# Generated by Django 3.2.9 on 2022-01-17 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('files', '0003_auto_20220117_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='SequenceLengthAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence_lengths', models.JSONField()),
                ('file', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='files.analysisfile')),
            ],
        ),
        migrations.CreateModel(
            name='DistancesBetweenResultsAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distances', models.JSONField()),
                ('file', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='files.resultfile')),
            ],
        ),
        migrations.CreateModel(
            name='DistancesAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distances', models.JSONField()),
                ('analysis_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.analysisfile')),
                ('result_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.resultfile')),
            ],
        ),
    ]
