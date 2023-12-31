# Generated by Django 4.2 on 2023-10-15 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_code', models.CharField(max_length=255)),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'Admin'), (2, 'Product Manager'), (3, 'Tester'), (4, 'Developer')])),
                ('created', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
