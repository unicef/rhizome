# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, IntegrityError
from django.core.exceptions import ObjectDoesNotExist

class Migration(migrations.Migration):

    dependencies = [
    # DELETE FROM django_migrations WHERE name = '0013_ingest_geojson';
        ('datapoints', '0010_ingest_geojson'),
    ]

    operations = [
        migrations.RunSQL(
        '''
        DROP TABLE IF EXISTS _tmp_som;
        CREATE TEMP TABLE _tmp_som (
        	source_object_code VARCHAR,
        	campaign_id INT
        );

        INSERT INTO _tmp_som
        (source_object_code,campaign_id)
        SELECT 'afghanistan-2014-04-01',7 UNION ALL
        SELECT 'afghanistan-2014-07-01',13 UNION ALL
        SELECT 'pakistan-2014-09-01',18 UNION ALL
        SELECT 'afghanistan-2014-10-01',19 UNION ALL
        SELECT 'pakistan-2014-10-01',20 UNION ALL
        SELECT 'afghanistan-2014-11-01',21 UNION ALL
        SELECT 'pakistan-2014-11-01',22 UNION ALL
        SELECT 'afghanistan-2014-12-01',23 UNION ALL
        SELECT 'pakistan-2014-12-01',24 UNION ALL
        SELECT 'afghanistan-2015-01-01',25 UNION ALL
        SELECT 'pakistan-2015-01-01',26 UNION ALL
        SELECT 'afghanistan-2015-02-01',27 UNION ALL
        SELECT 'pakistan-2015-02-01',28 UNION ALL
        SELECT 'afghanistan-2015-03-01',29 UNION ALL
        SELECT 'pakistan-2015-03-01',30 UNION ALL
        SELECT 'afghanistan-2015-05-01',33 UNION ALL
        SELECT 'afghanistan-january-2014',1 UNION ALL
        SELECT 'afghanistan-september-2014',1 UNION ALL
        SELECT 'afghanistan-february-2014',3 UNION ALL
        SELECT 'afghanistan-march-2014',5 UNION ALL
        SELECT 'afghanistan-may-2014',9 UNION ALL
        SELECT 'afghanistan-june-2014',11 UNION ALL
        SELECT 'afghanistan-august-2014',15 UNION ALL
        SELECT 'Sat Apr 04 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Sun Apr 05 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Mon Apr 06 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Wed Apr 08 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Thu Apr 09 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Mon Apr 13 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Wed Apr 15 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Thu Apr 16 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Sat Apr 18 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Sun Apr 19 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Mon Apr 20 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Wed Apr 22 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Thu Apr 23 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Sat Apr 25 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Sun Apr 26 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Mon Apr 27 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Tue Apr 28 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Wed Apr 29 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Thu Apr 30 00:00:00 UTC 2015',221 UNION ALL
        SELECT 'Sat Aug 01 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Sun Aug 02 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Mon Aug 03 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Tue Aug 04 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Wed Aug 05 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Thu Aug 06 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Fri Aug 07 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Sat Aug 08 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Tue Aug 09 00:00:00 UTC 2011',40 UNION ALL
        SELECT 'Sat Aug 09 00:00:00 UTC 2014',40 UNION ALL
        SELECT 'Sun Aug 09 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Mon Aug 10 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Tue Aug 11 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Wed Aug 12 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Thu Aug 13 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Fri Aug 14 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Sat Aug 15 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Sun Aug 16 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Mon Aug 17 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Tue Aug 18 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Wed Aug 19 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Thu Aug 20 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Fri Aug 21 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Sat Aug 22 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Sun Aug 23 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Mon Aug 24 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Tue Aug 25 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Wed Aug 26 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Sat Feb 01 00:00:00 UTC 2014',130 UNION ALL
        SELECT 'Sun Feb 01 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Mon Feb 23 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Wed Feb 25 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Thu Feb 26 00:00:00 UTC 2015',40 UNION ALL
        SELECT 'Wed Jan 01 00:00:00 UTC 2014',117 UNION ALL
        SELECT 'Thu Jan 01 00:00:00 UTC 2015',210 UNION ALL
        SELECT 'Thu Jan 02 00:00:00 UTC 2014',117 UNION ALL
        SELECT 'Fri Jan 03 00:00:00 UTC 2014',117 UNION ALL
        SELECT 'Sat Jan 04 00:00:00 UTC 2014',117 UNION ALL
        SELECT 'Sun Jan 05 00:00:00 UTC 2014',117 UNION ALL
        SELECT 'Mon Jan 06 00:00:00 UTC 2014',117 UNION ALL
        SELECT 'Tue Jan 07 00:00:00 UTC 2014',117 UNION ALL
        SELECT 'Sat Jan 11 00:00:00 UTC 2014',117 UNION ALL
        SELECT 'Tue Jan 21 00:00:00 UTC 2014',117 UNION ALL
        SELECT 'Tue Jul 01 00:00:00 UTC 2014',124 UNION ALL
        SELECT 'Wed Jul 01 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Thu Jul 02 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Fri Jul 03 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Sat Jul 04 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Sun Jul 05 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Mon Jul 06 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Tue Jul 07 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Wed Jul 08 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Thu Jul 09 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Fri Jul 10 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Sat Jul 11 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Sun Jul 12 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Mon Jul 13 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Tue Jul 14 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Wed Jul 15 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Thu Jul 16 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Fri Jul 17 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Sat Jul 18 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Sun Jul 19 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Mon Jul 20 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Tue Jul 21 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Wed Jul 22 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Thu Jul 23 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Fri Jul 24 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Sat Jul 25 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Sun Jul 26 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Mon Jul 27 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Tue Jul 28 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Wed Jul 29 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Thu Jul 30 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Fri Jul 31 00:00:00 UTC 2015',37 UNION ALL
        SELECT 'Mon Jun 01 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Tue Jun 02 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Wed Jun 03 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Thu Jun 04 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Fri Jun 05 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Sat Jun 06 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Sun Jun 07 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Mon Jun 08 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Tue Jun 09 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Wed Jun 10 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Thu Jun 11 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Fri Jun 12 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Sat Jun 13 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Mon Jun 15 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Tue Jun 16 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Wed Jun 17 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Thu Jun 18 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Fri Jun 19 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Sat Jun 20 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Sun Jun 21 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Mon Jun 22 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Tue Jun 23 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Wed Jun 24 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Thu Jun 25 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Fri Jun 26 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Sat Jun 27 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Sun Jun 28 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Mon Jun 29 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Tue Jun 30 00:00:00 UTC 2015',223 UNION ALL
        SELECT 'Sun Mar 01 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Tue Mar 03 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Wed Mar 04 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Thu Mar 05 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Fri Mar 06 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Mon Mar 09 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Fri Mar 13 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Sat Mar 14 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Sun Mar 15 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Mon Mar 16 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Tue Mar 17 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Wed Mar 18 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Sat Mar 21 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Tue Mar 24 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Wed Mar 25 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Mon Mar 30 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Tue Mar 31 00:00:00 UTC 2015',212 UNION ALL
        SELECT 'Fri May 01 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Sat May 02 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Sun May 03 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Mon May 04 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Fri May 08 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Mon May 11 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Tue May 12 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Wed May 13 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Thu May 14 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Fri May 15 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Sun May 17 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Mon May 18 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Wed May 20 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Sat May 23 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Sun May 24 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Mon May 25 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Tue May 26 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Wed May 27 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Thu May 28 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'Fri May 29 00:00:00 UTC 2015',222 UNION ALL
        SELECT 'nigeria-2014-01-01',117 UNION ALL
        SELECT 'nigeria-2014-03-01',108 UNION ALL
        SELECT 'nigeria-2014-04-01',115 UNION ALL
        SELECT 'nigeria-2014-05-01',125 UNION ALL
        SELECT 'nigeria-2014-06-01',111 UNION ALL
        SELECT 'nigeria-2014-08-01',104 UNION ALL
        SELECT 'nigeria-2014-09-01',128 UNION ALL
        SELECT 'nigeria-2014-11-01',100 UNION ALL
        SELECT 'Fri Apr 10 00:00:00 UTC 2015',210 UNION ALL
        SELECT 'pakistan-april-2014',8 UNION ALL
        SELECT 'pakistan-august-2014',16 UNION ALL
        SELECT 'pakistan-february-2014',4 UNION ALL
        SELECT 'pakistan-january-2014',2 UNION ALL
        SELECT 'pakistan-july-2014',14 ;

        UPDATE source_object_map som
        SET master_object_id = t.campaign_id
        FROM _tmp_som t
        WHERE som.source_object_code = t.source_object_code
        AND som.content_Type = 'campaign';

        INSERT INTO source_object_map
        (content_type, source_object_code, master_object_id, mapped_by_id)

        SELECT
        	'campaign'
        	,t.source_object_code
        	,t.campaign_id
        	,1
        FROM _tmp_som t
        WHERE NOT EXISTS (
        	SELECT 1 FROM source_object_map som
        	WHERE t.source_object_code = som.source_object_code
        );

        -- now delete campaing maps that dont exists.. still need to deal
        -- with the greater FK issue here..

        DELETE FROM doc_object_map
        WHERE source_object_map_id in (
        SELECT id from source_object_map
        where content_type = 'campaign'
        and master_object_id not in ( select id from campaign ));

        DELETE FROM source_object_map
        WHERE content_type = 'campaign'
        and master_object_id not in ( select id from campaign );


        '''
        )
    ]
