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

    OUTFILE = '/Users/johnd/code/polio/bin/polio_sample_data.json'

    tables_to_sync = ['campaign_type','region_type','office','campaign',
        'region','indicator','datapoint','calculated_indicator_component']

    for t in tables_to_sync:

        table_df = pd.read_excel('/Users/johnd/Desktop/polio_test_data.xls',\
            sheetname=t)
        results_dict[t] = table_df.to_dict()

    with open('bin/polio_test_data.json', 'w') as f:
      json.dump(results_dict, f, default=dthandler)

    print json.dumps(results_dict)
if __name__ == "__main__":
    main()
