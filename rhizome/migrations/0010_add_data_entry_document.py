from django.db import models, migrations

from rhizome.models import Document

def add_data_entry_document(apps, schema_editor):

	new_doc = Document.objects.create(
		doc_title = 'Data Entry'
	)


class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(add_data_entry_document),
    ]

    dependencies = [
        ('rhizome', '0008_indicator_class_map_table'),
    ]
