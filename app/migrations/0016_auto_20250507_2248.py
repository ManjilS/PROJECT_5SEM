# Generated by Django 3.0.5 on 2025-05-07 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_merge_20250507_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.staff'),
        ),
    ]
