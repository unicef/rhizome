from django.shortcuts import render
from source_data.forms import DocumentForm
from source_data.models import Document
from django.shortcuts import render_to_response
from django.template import RequestContext

import xlrd
import csv

def file_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

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

def process_xls():

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

    print df
