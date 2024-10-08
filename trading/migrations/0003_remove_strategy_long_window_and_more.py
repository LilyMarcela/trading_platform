# Generated by Django 4.2.16 on 2024-10-06 20:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trading', '0002_strategy_long_window_strategy_short_window'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='strategy',
            name='long_window',
        ),
        migrations.RemoveField(
            model_name='strategy',
            name='short_window',
        ),
        migrations.AddField(
            model_name='strategy',
            name='is_customizable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='strategy',
            name='is_prebuilt',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='strategy',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('paused', 'Paused'), ('completed', 'Completed')], default='active', max_length=20),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('risk_profile', models.CharField(choices=[('conservative', 'Conservative'), ('moderate', 'Moderate'), ('aggressive', 'Aggressive'), ('expert', 'Expert')], default='moderate', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StrategyConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter_name', models.CharField(max_length=255)),
                ('parameter_value', models.CharField(max_length=255)),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='configurations', to='trading.strategy')),
            ],
        ),
    ]
