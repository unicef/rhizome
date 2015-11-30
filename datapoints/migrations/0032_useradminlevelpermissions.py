# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.contrib.auth.models import User, Group

from datapoints.models import UserAdminLevelPermission,UserGroup

def pop_user_location_type_permission(apps, schema_editor):

    for u in User.objects.all():
        UserAdminLevelPermission.objects.create(
            user = u, location_type_id = 1
        )

    ## add all permissions for demo_user so i dont block developer work ##
    demo_user_obj = User.objects.get(username='demo_user')
    UserGroup.objects.all().delete()
    for g in Group.objects.all():
        UserGroup.objects.create(user=demo_user_obj, group=g)

    ## change the ufadmin group to manage_system ##
    g = Group.objects.get(name='ufadmin')
    g.name = 'manage_system'
    g.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datapoints', '0031_adminlevelpermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAdminLevelPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location_type', models.ForeignKey(to='datapoints.LocationType')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_admin_level_permission',
            },
        ),
        migrations.RunPython(
            pop_user_location_type_permission
        ),
    ]
