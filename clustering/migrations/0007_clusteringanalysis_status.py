# Generated by Django 3.2.9 on 2022-01-18 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clustering', '0006_scoringanalysis'),
    ]

    operations = [
        migrations.AddField(
            model_name='clusteringanalysis',
            name='status',
            field=models.CharField(choices=[('IP', 'IN_PROGRESS'), ('FA', 'FAILED'), ('SU', 'SUCCEEDED'), ('UN', 'UNKNOWN')], default='UN', max_length=2),
        ),
    ]
