# Generated by Django 3.0.5 on 2025-07-06 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_merge_20250621_0824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_leave',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='student_leave',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='attendance_report',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.student'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
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
            model_name='student_feedback',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student'),
        ),
        migrations.AlterField(
            model_name='student_leave',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student'),
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
    ]
