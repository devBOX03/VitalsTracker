import csv
import pandas as pd

from models import AggregatedVitalInfo

AGGREGATED_VITAL_INFO_CSV_FILE_NAME = 'aggregated_vital_info.csv'
DATA_PATH = 'data/'
AGGREGATED_VITAL_INFO_CSV_FILE_PATH = DATA_PATH + AGGREGATED_VITAL_INFO_CSV_FILE_NAME

def getDefaultResponseTemplate():
    return {
        'status': 'failed',
        'message': ''
    }

def getAggregatedDataDictTemplate():
    """return empty aggretaed data template"""
    return {
        "avg_hr": 0,
        "avg_rr": 0,
        "max_hr": 0,
        "min_hr": 0,
        "seg_end": 0,
        "seg_start": 0,
        "user_id": None
    }

def overwriteCSVData():
    with open(AGGREGATED_VITAL_INFO_CSV_FILE_PATH, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(AggregatedVitalInfo.AGGREGATED_COLUMN_NAME_LIST)

def storeDataInCSV(row):
    try:
        with open(AGGREGATED_VITAL_INFO_CSV_FILE_PATH, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row)
    except Exception:
        return False
    return True

def getFinalAggregatedData(user_id, row_aggregation_count):
    aggreagted_df = pd.read_csv(AGGREGATED_VITAL_INFO_CSV_FILE_PATH)
    final_aggregated_data = []
    intermediate_aggregated_data = getAggregatedDataDictTemplate()
    # filter data on user_id basis
    filtered_df = aggreagted_df.loc[aggreagted_df[AggregatedVitalInfo.USER_ID] == user_id]

    # row grouping
    row_number = 0
    for _, row in filtered_df.iterrows():
        row_number += 1

        if intermediate_aggregated_data[AggregatedVitalInfo.USER_ID] is None:
            intermediate_aggregated_data = dict(row)
        else:
            intermediate_aggregated_data[AggregatedVitalInfo.SEG_END] = row[AggregatedVitalInfo.SEG_END]
            intermediate_aggregated_data[AggregatedVitalInfo.AVG_HEART_RATE] += row[AggregatedVitalInfo.AVG_HEART_RATE]
            intermediate_aggregated_data[AggregatedVitalInfo.AVG_RESPIRATION_RATE] += row[AggregatedVitalInfo.AVG_RESPIRATION_RATE]
            intermediate_aggregated_data[AggregatedVitalInfo.MAX_HEART_RATE] = max(intermediate_aggregated_data[AggregatedVitalInfo.MAX_HEART_RATE],
                                                                                   row[AggregatedVitalInfo.MAX_HEART_RATE])
            intermediate_aggregated_data[AggregatedVitalInfo.MIN_HEART_RATE] = min(intermediate_aggregated_data[AggregatedVitalInfo.MIN_HEART_RATE],
                                                                                   row[AggregatedVitalInfo.MIN_HEART_RATE])

        # calculate and store row aggregation data
        if row_number % row_aggregation_count == 0:
            intermediate_aggregated_data[AggregatedVitalInfo.AVG_HEART_RATE] //= row_aggregation_count
            intermediate_aggregated_data[AggregatedVitalInfo.AVG_RESPIRATION_RATE] //= row_aggregation_count
            final_aggregated_data.append(dict(intermediate_aggregated_data))
            intermediate_aggregated_data = getAggregatedDataDictTemplate()

        # prevent data loss for remaining rows which doesn't fall under row_aggregation_count
        if row_number == len(filtered_df):
            intermediate_aggregated_data[AggregatedVitalInfo.AVG_HEART_RATE] //= (row_number % row_aggregation_count)
            intermediate_aggregated_data[AggregatedVitalInfo.AVG_RESPIRATION_RATE] //= (row_number % row_aggregation_count)
            final_aggregated_data.append(dict(intermediate_aggregated_data))

    return final_aggregated_data
