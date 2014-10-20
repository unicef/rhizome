import pprint as pp

import xlrd
import pandas as pd

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from pandas.io.excel import read_excel

from source_data.models import *
from datapoints.models import DataPoint, Source


class DocTransform(object):

    def __init__(self,document_id):

        self.source_datapoints = []
        # self.document_id = document_id
        self.document = Document.objects.get(id=document_id)
        self.file_path = settings.MEDIA_ROOT + str(self.document.docfile)
            # str(Document.objects.get(id=document_id).docfile)
        self.df = self.create_df()

    def create_df(self):

        if self.file_path.endswith('.csv'):
            df = pd.read_csv(self.file_path)
        else:
            wb = xlrd.open_workbook(self.file_path)
            sheet = wb.sheets()[0]

            df = read_excel(self.file_path,sheet.name)

        return df

    def get_essential_columns(self):

        header_list = list(self.df.columns.values)
        header_list_str = [str(col) for col in header_list]

        overrides = HeaderOverride.objects.filter(header_string__in=header_list_str)


        return overrides
