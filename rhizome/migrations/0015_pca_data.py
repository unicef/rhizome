from django.db import models, migrations
from django.conf import settings
from rhizome.models import *
import pandas as pd
import numpy as np
from django.core.exceptions import ObjectDoesNotExist
from rhizome.etl_tasks.transform_upload import ComplexDocTransform
from rhizome.etl_tasks.refresh_master import MasterRefresh
from rhizome.agg_tasks import AggRefresh

# psql rhizome -c "DELETE FROM django_migrations where name = '0015_pca_data';"

def ingest_pca_data(apps, schema_editor):

	indicator_names = ['# children seen - PCA',\
	'# children missed due to refusal - PCA',\
	'# children missed due to not available - PCA',\
	'# children missed due to no team visit - PCA',\
	'# children missed due to other reasons - PCA']

	indicator_name_to_id = upsert_indicators_delete_dps(indicator_names)
	df, campaign_names = upload_and_alter_csv(indicator_name_to_id)
	transform_df(df, indicator_names, campaign_names)
	# raise Exception('not done writing migration!')

def upsert_indicators_delete_dps(indicator_names):

	indicator_name_to_id = {}

	for indicator_name in indicator_names:
		ind_id = Indicator.objects.get_or_create(name=indicator_name, short_name=indicator_name, data_format='int')[0].id
		indicator_name_to_id[indicator_name] = ind_id

		DataPoint.objects.filter(indicator_id = ind_id).delete()
		DataPointComputed.objects.filter(indicator_id = ind_id).delete()
		DocDataPoint.objects.filter(indicator_id = ind_id).delete()

	return indicator_name_to_id

def transform_df(df, indicator_names, campaign_names):
	user_id = 1
	new_doc, created = Document.objects.get_or_create(
		doc_title = 'pca_data',
		guid = 'pca_data'
	)

	dt = ComplexDocTransform(user_id, new_doc.id, df)
	dt.main()
	ss_id_list = SourceSubmission.objects.filter(document_id = new_doc.id)
	print 'ss_id_list'
	print len(ss_id_list)
	# update the source_object_map master_ids for campaigns and indicators
	campaign_soms = SourceObjectMap.objects.filter(content_type='campaign')
	for campaign_som in campaign_soms:
		campaign = Campaign.objects.get(name=campaign_som.source_object_code)
		campaign_som.master_object_id = campaign.id
		campaign_som.save()

	indicator_soms = SourceObjectMap.objects.filter(content_type='indicator', source_object_code__in=indicator_names)
	for indicator_som in indicator_soms:
		indicator = Indicator.objects.get(name=indicator_som.source_object_code)
		indicator_som.master_object_id = indicator.id
		indicator_som.save()

	# run master refresh
	mr = MasterRefresh(user_id, new_doc.id)
	mr.main()
	dps = DataPoint.objects.filter(source_submission__in = ss_id_list)
	print 'len(dps)'
	print len(dps)

	# and aggRefresh
	campaign_ids = Campaign.objects.filter(name__in = campaign_names).values_list('id', flat=True)
	for campaign_id in campaign_ids:
		ar = AggRefresh(campaign_id)
	cdps = DataPointComputed.objects.filter(campaign_id__in = campaign_ids)
	print 'len(cdps)'
	print len(cdps)

	# now check the values
	# check_df = df[indicator_names]
	# print 'check_df'
	# print check_df
	# total_valid_values = 0
	# for idx, row in check_df.iterrows():
	# 	for name in indicator_names:
	# 		if row[name] and row[name] != 0:
	# 			total_valid_values += 1

	# print total_valid_values



def upload_and_alter_csv(indicator_name_to_id):
	xl = pd.ExcelFile('migration_data/T11-Situational-Dashboard-Data.xlsx')
	campaigns = xl.sheet_names
	dfs =[]
	for campaign in campaigns:
		df = xl.parse(campaign)
		df['unique_key'] = df['geocode'] + campaign
		df['campaign'] = campaign
		dfs.append(df)

	return (pd.concat(dfs), campaigns)

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0014_afp_cases'),
    ]

    operations = [
        migrations.RunPython(ingest_pca_data)
    ]
