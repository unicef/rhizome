import xlrd, csv, pandas

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from pandas.io.excel import read_excel

from source_data.forms import DocumentForm
from source_data.models import Document


def file_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            file_path = newdoc.docfile.url

            if file_path.endswith('xls') or file_path.endswith('xlsx'):
                process_xls(file_path)

    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'datapoints/file_upload.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )



def process_xls(f_path):

    f_path = '/Users/johndingee_seed/code/polio/media/documents/2014/09/16/SocMob.xlsx'

    wb = xlrd.open_workbook(f_path)

    for sheet in wb.sheets():
        # process_sheet(sheet)

        if sheet.nrows == 0:
            pass
        else:
            process_sheet(f_path,sheet.name)


def process_sheet(file_path,sheet_name):

    df = read_excel(file_path,sheet_name)

    cols = [col.lower() for col in df]

    row_basics = {}


    for i,(row) in enumerate(df.values):

        if i == 5:

            region_string = row[cols.index('lga')] + '-' + row[cols.index('state')] \
                + '-' + row[cols.index('ward')] + '-' + str(row[cols.index('settlement')])

            row_basics['row_number'] = i
            row_basics['region_string'] = region_string
            row_basics['uniquesoc'] = row[cols.index('uniquesoc')]
            row_basics['datesoc'] = str(row[cols.index('datesoc')])

            for i,(cell) in enumerate(row):

                to_create = row_basics
                to_create['indicator_string'] = cols[i]
                to_create['cell_value'] = cols[i]

                print to_create
