# Generated by Django 3.0.5 on 2025-04-28 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20250428_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='session_year_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.Session_year'),
        ),
    ]
