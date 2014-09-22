import xlrd, csv, pandas

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import IntegrityError
from django.contrib import messages

from pandas.io.excel import read_excel

from source_data.forms import DocumentForm
from source_data.models import Document,CsvUpload,ProcessStatus


def file_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.created_by = request.user
            newdoc.save()

            file_path = newdoc.docfile.url

            if file_path.endswith('xls') or file_path.endswith('xlsx'):
                process_xls(file_path,newdoc.id)

                return document_review(request,newdoc.id)


            else:
                messages.add_message(request, messages.INFO, 'Please\
                    upload either .CSV, .XLS or .XLSX file format')

    else:
        form = DocumentForm() # A empty, unbound form

    return render_to_response(
        'upload/file_upload.html',
        {'form': form},
        context_instance=RequestContext(request)
    )


def view_all_docs():
    # documents = Document.objects.all()

    # THIS CAN BE CLASS BASED
    pass

def process_xls(f_path,document_id):
    print 'SHIT IS HAPPENING \n' * 10

    wb = xlrd.open_workbook(f_path)

    for sheet in wb.sheets():
        # process_sheet(sheet)

        if sheet.nrows == 0:
            pass
        else:
            process_sheet(f_path,sheet.name,document_id)


def process_sheet(file_path,sheet_name,document_id):

    print 'PROCESSING SHEET!!'
    df = read_excel(file_path,sheet_name)

    cols = [col.lower() for col in df]

    row_basics = {}


    for i,(row) in enumerate(df.values):

        region_string = row[cols.index('lga')] + '-' + row[cols.index('state')] \
            + '-' + row[cols.index('ward')] + '-' + str(row[cols.index('settlement')])

        row_basics['row_number'] = i
        row_basics['region_string'] = region_string
        row_basics['campaign_string'] = str(row[cols.index('datesoc')])
        # row_basics['uniquesoc'] = row[cols.index('uniquesoc')]

        for i,(cell) in enumerate(row):

            print cell
            to_create = row_basics
            to_create['column_value'] = cols[i]
            to_create['cell_value'] = cell
            to_create['status_id'] = ProcessStatus.objects.get(status_text='TO_PROCESS').id
            to_create['document_id'] = document_id

            try:
                CsvUpload.objects.create(**to_create)

            except IntegrityError as e:
                print e


def ingest_document_to_master(request, document_id):

    print 'PERFORMING SOME ETL!'

    return document_review(request)



def document_review(request, document_id):

    print 'reviewing document'

    return render_to_response(
        'upload/document_review.html',
        # {'': form},
        context_instance=RequestContext(request)
    )
