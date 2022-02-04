#!/usr/bin/python
import json
import random
import requests
import pandas as pd

from app import HOSTNAME, PORT_NUMBER
from models import AggregatedVitalInfo
from service import VITALS_INPUT_POST

class VitalSimulator(object):

    # simulated data columns
    USER_ID = "user_id"
    TIMESTAMP = "timestamp"
    HEART_RATE = "heart_rate"
    RESPIRATION_RATE = "respiration_rate"
    ACTIVITY = "activity"

    SIMULATED_DATA_JSON_FILE_NAME = 'data/simulated_data.json'

    def __init__(self):
        self.final_df = pd.DataFrame(columns=AggregatedVitalInfo.AGGREGATED_COLUMN_NAME_LIST)
        self.intermediate_df = pd.DataFrame(columns=AggregatedVitalInfo.AGGREGATED_COLUMN_NAME_LIST)
        self.overwrite_json_file = True
        self.simulated_data = []

    def simulateData(self, user_id, start_timestamp, end_timestamp):
        print("Simulating and processing data for:=> %s" % user_id)
        for timestamp in range(start_timestamp, end_timestamp):
            heart_rate = random.randint(40,100)
            respiration_rate = random.randint(8,20)
            activity = random.randint(1,10)
            data = {
                self.USER_ID: user_id,
                self.TIMESTAMP: timestamp,
                self.HEART_RATE: heart_rate,
                self.RESPIRATION_RATE: respiration_rate,
                self.ACTIVITY: activity
            }
            self._processData(data)
            self.simulated_data.append(data)
        self._writeSimulatedDataToJsonFile()
        self._storeAggregatedData()
        # reset final and intermediate dataframe for next user
        self.intermediate_df = pd.DataFrame(columns=AggregatedVitalInfo.AGGREGATED_COLUMN_NAME_LIST)
        self.final_df = pd.DataFrame(columns=AggregatedVitalInfo.AGGREGATED_COLUMN_NAME_LIST)
        print("%s's vitals data simulation is done :)" % user_id)
    
    def _processData(self, data):
        # store intermediate data till timestamp reaches 15 mins
        self.intermediate_df.loc[len(self.intermediate_df)] = [data[self.USER_ID], data[self.TIMESTAMP], data[self.TIMESTAMP], data[self.HEART_RATE],
                                                     data[self.HEART_RATE], data[self.HEART_RATE], data[self.RESPIRATION_RATE]]
        
        # once timestamp count matches 15 mins, calculate and store final data from intermediate data
        if len(self.intermediate_df) >= AggregatedVitalInfo.MINIMUM_AGGREGATED_SECONDS:
            seg_start = self.intermediate_df.at[0, AggregatedVitalInfo.SEG_START]
            seg_end = self.intermediate_df.at[AggregatedVitalInfo.MINIMUM_AGGREGATED_SECONDS-1, AggregatedVitalInfo.SEG_END]
            avg_heart_rate = int(self.intermediate_df[AggregatedVitalInfo.AVG_HEART_RATE].mean())
            min_heart_rate = int(self.intermediate_df[AggregatedVitalInfo.MIN_HEART_RATE].min())
            max_heart_rate = int(self.intermediate_df[AggregatedVitalInfo.MAX_HEART_RATE].max())
            avg_respiration_rate = int(self.intermediate_df[AggregatedVitalInfo.AVG_RESPIRATION_RATE].mean())

            # write to final data frame
            self.final_df.loc[len(self.final_df)] = [data[self.USER_ID], seg_start, seg_end, avg_heart_rate,
                                                     min_heart_rate, max_heart_rate, avg_respiration_rate]
            # reset for next batch
            self.intermediate_df = pd.DataFrame(columns=AggregatedVitalInfo.AGGREGATED_COLUMN_NAME_LIST)

    def _writeSimulatedDataToJsonFile(self):
        file_operation_mode = 'w' if self.overwrite_json_file else 'a'
        self.overwrite_json_file = False
        with open(self.SIMULATED_DATA_JSON_FILE_NAME, file_operation_mode, encoding='utf-8') as json_file:
            json.dump(self.simulated_data, json_file, ensure_ascii=False, indent=4)
    
    def _storeAggregatedData(self):
        url = 'http://%s:%s/%s' % (HOSTNAME, PORT_NUMBER, VITALS_INPUT_POST)

        for _, row in self.final_df.iterrows():
            response = requests.post(url, json=dict(row))            
            try:
                response_text = json.loads(response.text)
            except Exception:
                response_text = None
            if response_text and response_text['status'] == 'failed':
                print(response['message'])
                break


if __name__ == '__main__':
    vts = VitalSimulator()
    vts.simulateData('Mike', 1589461200, 1589471320)
    vts.simulateData('Monika', 1589461200, 1589471320)
    vts.simulateData('Joe', 1589461200, 1589471320)
    vts.simulateData('Sam', 1589461200, 1589471320)
