# Generated by Django 4.2.4 on 2023-08-12 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_habitlog_habit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitlog',
            name='habit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.habit'),
        ),
    ]
