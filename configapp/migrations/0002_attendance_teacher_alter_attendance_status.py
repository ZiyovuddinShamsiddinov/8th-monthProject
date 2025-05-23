# Generated by Django 5.2 on 2025-05-03 19:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='configapp.teacher'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
