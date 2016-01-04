# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datapoints', '0039_top_lvl_indicator_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('top_lvl_location', models.ForeignKey(to='datapoints.Location')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'location_permission',
            },
        ),
        migrations.AlterField(
            model_name='adminlevelpermission',
            name='location_type',
            field=models.ForeignKey(default=1, to='datapoints.LocationType'),
        ),
    ]
