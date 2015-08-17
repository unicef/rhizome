# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0013_auto_20150816_0942'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentSourceObjectctMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.ForeignKey(to='source_data.Document')),
                ('source_object_map', models.ForeignKey(to='source_data.SourceObjectMap')),
            ],
            options={
                'db_table': 'document_to_source_object_map',
            },
        ),
        migrations.AlterUniqueTogether(
            name='documentsourceobjectctmap',
            unique_together=set([('document', 'source_object_map')]),
        ),
    ]
