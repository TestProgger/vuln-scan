# Generated by Django 4.2.7 on 2023-12-07 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scenarios', '0007_alter_scenario_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenarioblock',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='scenarios.scenarioblock'),
        ),
    ]
