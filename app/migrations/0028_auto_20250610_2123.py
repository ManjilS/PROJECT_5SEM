# Generated by Django 3.0.5 on 2025-06-10 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20250605_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff_feedback',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.staff'),
        ),
        migrations.AlterField(
            model_name='staff_leave',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.staff'),
        ),
        migrations.AlterField(
            model_name='staff_notification',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.staff'),
        ),
        migrations.AlterField(
            model_name='student_notification',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.staff'),
        ),
        migrations.CreateModel(
            name='student_leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_start_date', models.DateField()),
                ('leave_end_date', models.DateField()),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student')),
            ],
        ),
    ]
