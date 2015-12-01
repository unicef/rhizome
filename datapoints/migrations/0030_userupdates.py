# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import Group
from django.conf import settings


def upsert_user_roles(apps, schema_editor):

    new_groups = ['data_entry','manage_system','dashboard_builder','source_data']

    Group.objects.all().delete()
    for g in new_groups:
        Group.objects.create(name=g)

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datapoints', '0029_mingeo'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationResponsibility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.ForeignKey(to='datapoints.Location')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'location_responsibility',
            },
        ),
        migrations.AlterUniqueTogether(
            name='locationpermission',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='locationpermission',
            name='location',
        ),
        migrations.RemoveField(
            model_name='locationpermission',
            name='user',
        ),
        migrations.DeleteModel(
            name='LocationPermission',
        ),
        migrations.AlterUniqueTogether(
            name='locationresponsibility',
            unique_together=set([('user', 'location')]),
        ),
        migrations.RunPython(
            upsert_user_roles,
        ),
    ]
