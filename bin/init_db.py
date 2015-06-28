import pandas as pd
import json
import datetime

def main():

    results_dict = {}

    dthandler = lambda obj: (
         obj.isoformat()
         if isinstance(obj, datetime.datetime)
         or isinstance(obj, datetime.date)
         else None)

    INFILE = '/Users/john/code/polio/bin/polio_test_data.xls'

    tables_to_sync = ['campaign_type','region_type','office','campaign',
        'region','indicator','datapoint','calculated_indicator_component']

    for t in tables_to_sync:

        table_df = pd.read_excel(INFILE,sheetname=t)

        print table_df[:1]
        results_dict[t] = table_df.to_dict()


    print json.dumps(results_dict)
if __name__ == "__main__":
    main()
