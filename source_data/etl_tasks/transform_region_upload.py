import sys
from pandas import DataFrame

sys.path.append('/Users/johndingee_seed/code/polio')
from source_data.models import SourceRegion



SOURCE_FILE = '/Users/johndingee_seed/Desktop/ng_regions.csv'


def file_to_df():

    df = DataFrame.from_csv(SOURCE_FILE)
    print df



if __name__ == "__main__":
    file_to_df()
