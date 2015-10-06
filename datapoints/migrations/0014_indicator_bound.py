# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import User
from datapoints import cache_tasks

def cache_metadata(apps, schema_editor):

    indicator_cache_data = cache_tasks.cache_indicator_abstracted()

class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0013_clean_doc_table'),
    ]

    operations = [

    migrations.RunSQL("""

    DROP TABLE IF EXISTS _bound;
    CREATE TABLE _bound AS

    SELECT 168 as indicator_id ,-1 as mn_val ,0 as mx_val ,'good' as bound_name UNION ALL
    SELECT 168,0,NULL,'bad' UNION ALL
    SELECT 431,0,0.05,'good' UNION ALL
    SELECT 432,0,0.05,'good' UNION ALL
    SELECT 169,0,0.75,'bad' UNION ALL
    SELECT 233,0,0.75,'bad' UNION ALL
    SELECT 173,0,0.75,'bad' UNION ALL
    SELECT 172,0,0.49,'bad' UNION ALL
    SELECT 174,0,0.85,'bad' UNION ALL
    SELECT 178,0,0.5,'bad' UNION ALL
    SELECT 224,0,0.75,'bad' UNION ALL
    SELECT 179,0,0.75,'bad' UNION ALL
    SELECT 180,0,0.75,'bad' UNION ALL
    SELECT 230,0,0.75,'bad' UNION ALL
    SELECT 239,0,0.5,'bad' UNION ALL
    SELECT 461,0,0.9,'bad' UNION ALL
    SELECT 228,0,0.75,'bad' UNION ALL
    SELECT 184,0,0.75,'bad' UNION ALL
    SELECT 194,0,0.001,'good' UNION ALL
    SELECT 185,0,0.75,'bad' UNION ALL
    SELECT 226,0,0.75,'bad' UNION ALL
    SELECT 222,0,0.75,'bad' UNION ALL
    SELECT 166,0,0.0049,'good' UNION ALL
    SELECT 187,0,0.74,'bad' UNION ALL
    SELECT 164,0,0.009,'good' UNION ALL
    SELECT 189,0,0.59,'bad' UNION ALL
    SELECT 245,0,0.6,'bad' UNION ALL
    SELECT 236,0,0.6,'bad' UNION ALL
    SELECT 191,0,0.75,'good' UNION ALL
    SELECT 193,0,0.6,'bad' UNION ALL
    SELECT 219,0,0.75,'bad' UNION ALL
    SELECT 194,0.001,0.1,'ok' UNION ALL
    SELECT 166,0.0049,0.01,'ok' UNION ALL
    SELECT 164,0.009,0.02,'ok' UNION ALL
    SELECT 166,0.01,1,'bad' UNION ALL
    SELECT 164,0.02,1,'bad' UNION ALL
    SELECT 431,0.05,0.09,'ok' UNION ALL
    SELECT 432,0.05,0.09,'ok' UNION ALL
    SELECT 431,0.09,1,'bad' UNION ALL
    SELECT 432,0.09,1,'bad' UNION ALL
    SELECT 194,0.1,1,'bad' UNION ALL
    SELECT 172,0.49,0.79,'ok' UNION ALL
    SELECT 178,0.5,0.75,'ok' UNION ALL
    SELECT 239,0.5,0.75,'ok' UNION ALL
    SELECT 189,0.59,0.8,'ok' UNION ALL
    SELECT 245,0.6,0.79,'ok' UNION ALL
    SELECT 236,0.6,0.79,'ok' UNION ALL
    SELECT 193,0.6,0.79,'ok' UNION ALL
    SELECT 187,0.74,0.9,'ok' UNION ALL
    SELECT 173,0.75,0.9,'ok' UNION ALL
    SELECT 178,0.75,1,'good' UNION ALL
    SELECT 224,0.75,0.9,'ok' UNION ALL
    SELECT 239,0.75,1,'good' UNION ALL
    SELECT 222,0.75,0.9,'ok' UNION ALL
    SELECT 219,0.75,0.9,'ok' UNION ALL
    SELECT 169,0.75,0.9,'ok' UNION ALL
    SELECT 233,0.75,0.9,'ok' UNION ALL
    SELECT 179,0.75,0.9,'ok' UNION ALL
    SELECT 180,0.75,0.9,'ok' UNION ALL
    SELECT 230,0.75,0.9,'ok' UNION ALL
    SELECT 228,0.75,0.9,'ok' UNION ALL
    SELECT 184,0.75,0.9,'ok' UNION ALL
    SELECT 185,0.75,0.9,'ok' UNION ALL
    SELECT 226,0.75,0.9,'ok' UNION ALL
    SELECT 191,0.75,0.9,'ok' UNION ALL
    SELECT 172,0.79,1,'good' UNION ALL
    SELECT 245,0.79,1,'good' UNION ALL
    SELECT 236,0.79,1,'good' UNION ALL
    SELECT 193,0.79,1,'good' UNION ALL
    SELECT 189,0.8,1,'good' UNION ALL
    SELECT 174,0.85,0.95,'ok' UNION ALL
    SELECT 169,0.9,1,'good' UNION ALL
    SELECT 173,0.9,1,'good' UNION ALL
    SELECT 233,0.9,1,'good' UNION ALL
    SELECT 224,0.9,1,'good' UNION ALL
    SELECT 179,0.9,1,'good' UNION ALL
    SELECT 180,0.9,1,'good' UNION ALL
    SELECT 230,0.9,1,'good' UNION ALL
    SELECT 461,0.9,0.9999,'ok' UNION ALL
    SELECT 228,0.9,1,'good' UNION ALL
    SELECT 184,0.9,1,'good' UNION ALL
    SELECT 185,0.9,1,'good' UNION ALL
    SELECT 226,0.9,1,'good' UNION ALL
    SELECT 222,0.9,1,'good' UNION ALL
    SELECT 187,0.9,1,'good' UNION ALL
    SELECT 219,0.9,1,'good' UNION ALL
    SELECT 191,0.9,1,'bad' UNION ALL
    SELECT 174,0.95,1,'good' UNION ALL
    SELECT 461,0.9999,1,'good' UNION ALL
    SELECT 431,1,NULL        ,'invalid' UNION ALL
    SELECT 432,1,NULL        ,'invalid' UNION ALL
    SELECT 169,1,NULL        ,'invalid' UNION ALL
    SELECT 233,1,NULL        ,'invalid' UNION ALL
    SELECT 172,1,NULL        ,'invalid' UNION ALL
    SELECT 219,1,NULL    ,'invalid' UNION ALL
    SELECT 174,1,NULL    ,'invalid' UNION ALL
    SELECT 178,1,NULL    ,'invalid' UNION ALL
    SELECT 179,1,NULL        ,'invalid' UNION ALL
    SELECT 180,1,NULL        ,'invalid' UNION ALL
    SELECT 230,1,NULL        ,'invalid' UNION ALL
    SELECT 239,1,NULL        ,'invalid' UNION ALL
    SELECT 228,1,NULL        ,'invalid' UNION ALL
    SELECT 184,1,NULL        ,'invalid' UNION ALL
    SELECT 185,1,NULL        ,'invalid' UNION ALL
    SELECT 226,1,NULL        ,'invalid' UNION ALL
    SELECT 222,1,NULL        ,'invalid' UNION ALL
    SELECT 166,1,NULL        ,'invalid' UNION ALL
    SELECT 187,1,NULL        ,'invalid' UNION ALL
    SELECT 164,1,NULL        ,'invalid' UNION ALL
    SELECT 189,1,NULL        ,'invalid' UNION ALL
    SELECT 245,1,NULL        ,'invalid' UNION ALL
    SELECT 236,1,NULL        ,'invalid' UNION ALL
    SELECT 191,1,NULL        ,'invalid' UNION ALL
    SELECT 193,1,NULL       ,'invalid' UNION ALL
    SELECT 168,NULL,-1,'invalid' UNION ALL
    SELECT 431,NULL,0,'invalid' UNION ALL
    SELECT 432,NULL,0,'invalid' UNION ALL
    SELECT 169,NULL,0,'invalid' UNION ALL
    SELECT 233,NULL,0,'invalid' UNION ALL
    SELECT 172,NULL,0,'invalid' UNION ALL
    SELECT 219,NULL,-1,'invalid' UNION ALL
    SELECT 174,NULL,0,'invalid' UNION ALL
    SELECT 178,NULL,0,'invalid' UNION ALL
    SELECT 179,NULL,0,'invalid' UNION ALL
    SELECT 180,NULL,0,'invalid' UNION ALL
    SELECT 230,NULL,0,'invalid' UNION ALL
    SELECT 239,NULL,0,'invalid' UNION ALL
    SELECT 228,NULL,0,'invalid' UNION ALL
    SELECT 184,NULL,0,'invalid' UNION ALL
    SELECT 185,NULL,0,'invalid' UNION ALL
    SELECT 226,NULL,0,'invalid' UNION ALL
    SELECT 222,NULL,0,'invalid' UNION ALL
    SELECT 166,NULL,0,'invalid' UNION ALL
    SELECT 187,NULL,0,'invalid' UNION ALL
    SELECT 164,NULL,0,'invalid' UNION ALL
    SELECT 189,NULL,0,'invalid' UNION ALL
    SELECT 245,NULL,0,'invalid' UNION ALL
    SELECT 236,NULL,0,'invalid' UNION ALL
    SELECT 191,NULL,0,'invalid' UNION ALL
    SELECT 193,NULL,0,'invalid';

    INSERT INTO indicator_bound
    (indicator_id, mn_val, mx_val, bound_name, direction)

    SELECT indicator_id, mn_val, mx_val, bound_name, 1
    FROM _bound;

    """),

    migrations.RunPython(
        cache_metadata,
    )

    ]
