# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datapoints', '0033_indicatortooffice'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndicatorClassMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string_value', models.CharField(max_length=100)),
                ('enum_value', models.IntegerField()),
                ('is_display', models.BooleanField()),
            ],
            options={
                'db_table': 'indicator_class_map',
            },
        ),
        # migrations.RenameField(
        #     model_name='campaign',
        #     old_name='management_dash_pct_complete',
        #     new_name='pct_complete',
        # ),
        migrations.RemoveField(
            model_name='campaign',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='customdashboard',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='location',
            name='slug',
        ),
        # migrations.AddField(
        #     model_name='campaign',
        #     name='name',
        #     field=models.CharField(default=1, max_length=255),
        #     preserve_default=False,
        # ),
        # migrations.AddField(
        #     model_name='campaign',
        #     name='top_lvl_indicator_tag',
        #     field=models.ForeignKey(default=1, to='datapoints.IndicatorTag'),
        #     preserve_default=False,
        # ),
        # migrations.AddField(
        #     model_name='campaign',
        #     name='top_lvl_location',
        #     field=models.ForeignKey(default=1, to='datapoints.Location'),
        #     preserve_default=False,
        # ),
        # migrations.AddField(
        #     model_name='locationpermission',
        #     name='top_lvl_location',
        #     field=models.ForeignKey(to='datapoints.Location'),
        # ),
        # migrations.AddField(
        #     model_name='locationpermission',
        #     name='user',
        #     field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        # ),
        migrations.AddField(
            model_name='indicatorclassmap',
            name='indicator',
            field=models.ForeignKey(to='datapoints.Indicator'),
        ),
        migrations.AlterUniqueTogether(
            name='indicatorclassmap',
            unique_together=set([('indicator', 'string_value', 'enum_value')]),
        ),
    ]
