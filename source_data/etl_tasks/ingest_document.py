def main(df):


    for i,(row) in enumerate(df.values):
        row_basics = {}

        region_string = row[cols.index('lga')] + '-' + row[cols.index('state')] \
            + '-' + row[cols.index('ward')] + '-' + str(row[cols.index('settlement')])

        row_basics['row_number'] = i
        row_basics['region_string'] = region_string
        row_basics['campaign_string'] = str(row[cols.index('datesoc')])
        # row_basics['uniquesoc'] = row[cols.index('uniquesoc')]

        for i,(cell) in enumerate(row):

            to_create = row_basics
            to_create['column_value'] = cols[i]
            to_create['cell_value'] = cell
            # to_create['status_id'] = ProcessStatus.objects.get(status_text='TO_PROCESS').id
            # to_create['document_id'] = document_id
            #
            # try:
            #     CsvUpload.objects.create(**to_create)
            #
            # except IntegrityError as e:
            #     print e
