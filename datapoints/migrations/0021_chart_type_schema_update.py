# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0020_chart_type_schema'),
    ]

    operations = [
        migrations.RunSQL('''

        INSERT INTO chart_type
        -- seed the chart type table --
        (name)
        SELECT 'PieChart';

        INSERT INTO chart_type_to_indicator
        (chart_type_id, indicator_id)
        SELECT ct.id, i.id
        FROM chart_type ct
        INNER JOIN indicator i
        ON ct.name = 'PieChart';

        DROP TABLE IF EXISTS chart_type_name_change;
        CREATE TEMP TABLE chart_type_name_change AS

        SELECT 'line' as oldName , 'LineChart' as newName UNION ALL
        SELECT 'bar' , 'BarChart' UNION ALL
        SELECT 'column','ColumnChart' UNION ALL
        SELECT 'map','ChoroplethMap' UNION ALL
        SELECT 'scatter','ScatterChart' UNION ALL
        SELECT 'matrix','MatrixChart';

        UPDATE chart_type ct
        SET name = x.newName
        FROM chart_type_name_change x
        WHERE x.oldName = ct.name;

        DROP TABLE IF EXISTS chart_type_name_change;

        -- Alter data so Ruoran Can test the endpoint  --

        DELETE FROM chart_type_to_indicator
        WHERE indicator_id = 168
        AND chart_type_id > 2;

        DELETE FROM chart_type_to_indicator
        WHERE indicator_id = 475
        AND chart_type_id > 3;

        DELETE FROM chart_type_to_indicator
        WHERE indicator_id = 22
        AND chart_type_id < 3;


        ''')
    ]
