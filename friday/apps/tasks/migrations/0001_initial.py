# Generated by Django 4.2 on 2023-10-07 18:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('issues', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Todo'), (2, 'Wip'), (3, 'Need Review'), (4, 'Need Changes'), (5, 'Done'), (6, 'Hold')], default=1)),
                ('notes', models.TextField(blank=True, null=True)),
                ('link', models.CharField(blank=True, max_length=255, null=True)),
                ('updated', models.DateField(default=django.utils.timezone.localdate)),
                ('created', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='issues.issue')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.PositiveSmallIntegerField(choices=[(1, 'Todo'), (2, 'Wip'), (3, 'Need Review'), (4, 'Need Changes'), (5, 'Done'), (6, 'Hold')])),
                ('new_status', models.PositiveSmallIntegerField(choices=[(1, 'Todo'), (2, 'Wip'), (3, 'Need Review'), (4, 'Need Changes'), (5, 'Done'), (6, 'Hold')])),
                ('notes', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tasks.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
