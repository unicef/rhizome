
import pandas as pd

class xlsProcessor(object):

    def __init__(self):

        self.config_dict = {
            'location_code_columns':[u'geocode'],
            'date_columns':['date'],
            'not_indicators':[]
        }

        self.xl = pd.ExcelFile('/Users/john/Desktop/Real.Data.Province.xlsx')
        self.output_file = '/Users/john/Desktop/RealDataCleaned.csv'
        self.location_code_column, self.date_column = 'geocode', 'date'

        self.dont_process = [self.location_code_column, self.date_column,\
            'District','Province Name','sn','LQAS_dist_754']
        self.result_list = []

    def main(self):

        all_sheets = self.xl.sheet_names

        for sht in all_sheets:
            self.process_sheet(sht)

        output_df = pd.DataFrame(self.result_list,\
            columns=['location_code','data_date','indicator_slug','value'])

        output_df.to_csv(self.output_file)

    def process_sheet(self, sht):

        sheet_df = self.xl.parse(sht)
        sheet_columns = list(sheet_df.columns)

        non_null_df = sheet_df.where((pd.notnull(sheet_df)), None)
        list_of_dicts = sheet_df.transpose().to_dict()

        for ix, row_data in list_of_dicts.iteritems():
            location_code = row_data[self.location_code_column]
            data_date = row_data[self.date_column]

            for k,v in row_data.iteritems():
                self.process_row(location_code, data_date, k, v)

    def process_row(self, l, d, k, v):

        try:
            if v.lower() == 'Yes':
                v = 1
            if v.lower() == 'No':
                v = 0
        except AttributeError:
            pass

        if k not in self.dont_process and v:
            self.result_list.append([l, d, k, v])

if __name__ == '__main__':
    x = xlsProcessor()
    x.main()
