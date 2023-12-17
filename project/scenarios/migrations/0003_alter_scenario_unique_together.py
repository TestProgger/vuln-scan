# Generated by Django 4.2.7 on 2023-12-13 21:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scenarios', '0002_alter_scenario_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='scenario',
            unique_together={('owner', 'hashsum', 'name')},
        ),
    ]
