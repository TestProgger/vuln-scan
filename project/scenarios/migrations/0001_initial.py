# Generated by Django 4.2.7 on 2023-12-13 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import project.utils.models.mixins
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('text', models.TextField()),
                ('value', models.JSONField()),
                ('hashsum', models.CharField(max_length=130)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'scenario',
            },
            bases=(models.Model, project.utils.models.mixins.PkUUIDModelMixin),
        ),
        migrations.CreateModel(
            name='ScenarioStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('code', models.CharField(db_index=True, max_length=255, unique=True)),
            ],
            options={
                'db_table': 'scenario_status',
            },
            bases=(models.Model, project.utils.models.mixins.PkUUIDModelMixin),
        ),
        migrations.CreateModel(
            name='ScenarioBlock',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('instruction', models.CharField(blank=True, max_length=255, null=True)),
                ('parent_instruction', models.CharField(blank=True, max_length=255, null=True)),
                ('value', models.JSONField()),
                ('depend_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scenarios.scenarioblock')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='scenarios.scenarioblock')),
                ('scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenarios.scenario')),
            ],
            options={
                'db_table': 'scenario_block',
            },
            bases=(models.Model, project.utils.models.mixins.PkUUIDModelMixin),
        ),
        migrations.AddField(
            model_name='scenario',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scenarios.scenariostatus'),
        ),
    ]
