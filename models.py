class AggregatedVitalInfo:
    # aggregated data columns
    USER_ID = "user_id"
    SEG_START = "seg_start"
    SEG_END = "seg_end"
    AVG_HEART_RATE = "avg_hr"
    MIN_HEART_RATE = "min_hr"
    MAX_HEART_RATE = "max_hr"
    AVG_RESPIRATION_RATE = "avg_rr"

    AGGREGATED_COLUMN_NAME_LIST = [USER_ID, SEG_START, SEG_END, AVG_HEART_RATE, MIN_HEART_RATE, 
                                   MAX_HEART_RATE, AVG_RESPIRATION_RATE]
    MINIMUM_AGGREGATED_MINUTES = 15
    MINIMUM_AGGREGATED_SECONDS = MINIMUM_AGGREGATED_MINUTES * 60
