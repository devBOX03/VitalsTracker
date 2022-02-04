from flask import Flask, request, jsonify

from models import AggregatedVitalInfo
from service_handler import getDefaultResponseTemplate, storeDataInCSV, getFinalAggregatedData
from utils import HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_CODE_INTERNAL_ERROR, HTTP_STATUS_CODE_OKAY, \
    HTTP_STATUS_CODE_CREATED


app = Flask(__name__)

# urls
VITALS_INPUT_POST = '/vitals_input'
VITALS_OUTPUT_GET = '/vitals_output'

@app.route(VITALS_INPUT_POST, methods=['POST'])
def storeVitalInput():
    response = getDefaultResponseTemplate()
    if not request.json:
        response['message'] =  "Send data in json format!"
        return jsonify(response)

    user_id = request.json.get('user_id')
    seg_start = request.json.get('seg_start')
    seg_end = request.json.get('seg_end')
    avg_hr = request.json.get('avg_hr')
    min_hr = request.json.get('min_hr')
    max_hr = request.json.get('max_hr')
    avg_rr = request.json.get('avg_rr')

    if not user_id or not seg_start or not seg_end or not avg_hr or not min_hr or not max_hr or not avg_rr:
        response['message'] =  "Check missing fields 'user_id', 'seg_start', 'seg_end', 'avg_hr', 'min_hr', 'max_hr', 'avg_rr'"
        return jsonify(response)

    row = [user_id, seg_start, seg_end, avg_hr, min_hr, max_hr, avg_rr]
    success = storeDataInCSV(row)
    if not success:
        response['message'] =  "Unable to store data due to some internal error"
        return jsonify(response), HTTP_STATUS_CODE_INTERNAL_ERROR

    response['status'] = 'success'
    response['message'] =  "Data has been saved successfully!"

    return jsonify(response), HTTP_STATUS_CODE_CREATED

@app.route(VITALS_OUTPUT_GET, methods=['GET'])
def getVitalsOutput():
    response = getDefaultResponseTemplate()
    row_aggregation_count = 1
    user_id = request.args.get('user_id')
    try:
        minutes = int(request.args.get('minutes', AggregatedVitalInfo.MINIMUM_AGGREGATED_MINUTES))
        if minutes % AggregatedVitalInfo.MINIMUM_AGGREGATED_MINUTES != 0:
            response['message'] = 'please provide minutes in 15 mins slot'
            return jsonify(response), HTTP_STATUS_BAD_REQUEST
        row_aggregation_count = minutes // AggregatedVitalInfo.MINIMUM_AGGREGATED_MINUTES
    except Exception:
        response['message'] = 'please provide minutes in number'
        return jsonify(response), HTTP_STATUS_BAD_REQUEST

    final_aggregated_data = getFinalAggregatedData(user_id, row_aggregation_count)    

    return jsonify(final_aggregated_data), HTTP_STATUS_CODE_OKAY
